import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreatePurchaseDto } from './dto/create-purchase.dto';

@Injectable()
export class PurchasesService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.purchase.findMany({
      include: {
        supplier: true,
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
    const purchase = await this.prisma.purchase.findUnique({
      where: { id },
      include: {
        supplier: true,
        user: { select: { id: true, name: true, email: true } },
        items: {
          include: {
            product: true,
          },
        },
      },
    });
    if (!purchase) {
      throw new NotFoundException(`Purchase with ID ${id} not found`);
    }
    return purchase;
  }

  async create(userId: number, dto: CreatePurchaseDto) {
    if (!dto.items || dto.items.length === 0) {
      throw new BadRequestException('Purchase must contain at least one item');
    }

    const supplier = await this.prisma.supplier.findUnique({
      where: { id: dto.supplierId },
    });
    if (!supplier) {
      throw new NotFoundException(`Supplier with ID ${dto.supplierId} not found`);
    }

    // Verify all products exist
    for (const item of dto.items) {
      const product = await this.prisma.product.findUnique({
        where: { id: item.productId },
      });
      if (!product) {
        throw new NotFoundException(`Product with ID ${item.productId} not found`);
      }
    }

    // Calculate total
    const total = dto.items.reduce(
      (sum, item) => sum + Number(item.costPrice) * item.quantity,
      0,
    );

    // Atomic transaction: Create purchase + items and increment product quantities
    return this.prisma.$transaction(async (tx) => {
      const purchase = await tx.purchase.create({
        data: {
          supplierId: dto.supplierId,
          userId,
          total,
          items: {
            create: dto.items.map((item) => ({
              productId: item.productId,
              quantity: item.quantity,
              costPrice: item.costPrice,
            })),
          },
        },
        include: {
          supplier: true,
          user: { select: { id: true, name: true, email: true } },
          items: {
            include: { product: true },
          },
        },
      });

      // Update product stocks
      for (const item of dto.items) {
        await tx.product.update({
          where: { id: item.productId },
          data: {
            quantity: {
              increment: item.quantity,
            },
          },
        });
      }

      return purchase;
    });
  }
}

