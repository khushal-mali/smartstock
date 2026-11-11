import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateSaleDto } from './dto/create-sale.dto';

@Injectable()
export class SalesService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.sale.findMany({
      include: {
        user: { select: { id: true, name: true, email: true } },
        items: {
          include: {
            product: true,
          },
        },
      },
      orderBy: { date: 'desc' },
    });
  }

  async findOne(id: number) {
    const sale = await this.prisma.sale.findUnique({
      where: { id },
      include: {
        user: { select: { id: true, name: true, email: true } },
        items: {
          include: {
            product: {
              include: {
                category: true,
                supplier: true,
              },
            },
          },
        },
      },
    });
    if (!sale) {
      throw new NotFoundException(`Sale with ID ${id} not found`);
    }
    return sale;
  }

  private async generateInvoiceNumber(): Promise<string> {
    const now = new Date();
    const yearMonth = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}`;
    const prefix = `INV-${yearMonth}-`;

    const count = await this.prisma.sale.count();
    const nextSeq = String(count + 1).padStart(4, '0');
    return `${prefix}${nextSeq}`;
  }

  async create(userId: number, dto: CreateSaleDto) {
    if (!dto.items || dto.items.length === 0) {
      throw new BadRequestException('Sale must contain at least one item');
    }

    // Step 1: Pre-validate all products and quantities
    const validatedItems: { productId: number; quantity: number; price: number; name: string }[] = [];

    for (const item of dto.items) {
      const product = await this.prisma.product.findUnique({
        where: { id: item.productId },
      });

      if (!product) {
        throw new NotFoundException(`Product with ID ${item.productId} not found`);
      }

      // Check stock availability
      if (item.quantity > product.quantity) {
        throw new BadRequestException(
          `Insufficient stock for '${product.name}' (SKU: ${product.sku}). Available: ${product.quantity}, Requested: ${item.quantity}`,
        );
      }

      const itemPrice = item.price !== undefined ? item.price : Number(product.price);
      validatedItems.push({
        productId: product.id,
        quantity: item.quantity,
        price: itemPrice,
        name: product.name,
      });
    }

    const total = validatedItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const invoiceNo = await this.generateInvoiceNumber();

    // Step 2: Atomic database transaction
    return this.prisma.$transaction(async (tx) => {
      // Create sale record
      const sale = await tx.sale.create({
        data: {
          invoiceNo,
          userId,
          total,
          items: {
            create: validatedItems.map((item) => ({
              productId: item.productId,
              quantity: item.quantity,
              price: item.price,
            })),
          },
        },
        include: {
          user: { select: { id: true, name: true, email: true } },
          items: {
            include: { product: true },
          },
        },
      });

      // Deduct stock from each product
      for (const item of validatedItems) {
        await tx.product.update({
          where: { id: item.productId },
          data: {
            quantity: {
              decrement: item.quantity,
            },
          },
        });
      }

      return sale;
    });
  }
}

