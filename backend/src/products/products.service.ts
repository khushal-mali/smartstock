import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';

@Injectable()
export class ProductsService {
  constructor(private prisma: PrismaService) {}

  async findAll(query?: { search?: string; categoryId?: number; lowStock?: boolean }) {
    const where: any = {};

    if (query?.search) {
      where.OR = [
        { name: { contains: query.search, mode: 'insensitive' } },
        { sku: { contains: query.search, mode: 'insensitive' } },
      ];
    }

    if (query?.categoryId) {
      where.categoryId = Number(query.categoryId);
    }

    const products = await this.prisma.product.findMany({
      where,
      include: {
        category: true,
        supplier: true,
      },
      orderBy: { name: 'asc' },
    });

    if (query?.lowStock) {
      return products.filter((p) => p.quantity <= p.reorderLevel);
    }

    return products;
  }

  async findOne(id: number) {
    const product = await this.prisma.product.findUnique({
      where: { id },
      include: {
        category: true,
        supplier: true,
      },
    });
    if (!product) {
      throw new NotFoundException(`Product with ID ${id} not found`);
    }
    return product;
  }

  async create(dto: CreateProductDto) {
    const existing = await this.prisma.product.findUnique({
      where: { sku: dto.sku.trim().toUpperCase() },
    });
    if (existing) {
      throw new ConflictException(`Product with SKU '${dto.sku}' already exists`);
    }

    // Verify category and supplier exist
    const category = await this.prisma.category.findUnique({ where: { id: dto.categoryId } });
    if (!category) throw new NotFoundException(`Category with ID ${dto.categoryId} not found`);

    const supplier = await this.prisma.supplier.findUnique({ where: { id: dto.supplierId } });
    if (!supplier) throw new NotFoundException(`Supplier with ID ${dto.supplierId} not found`);

    return this.prisma.product.create({
      data: {
        sku: dto.sku.trim().toUpperCase(),
        name: dto.name.trim(),
        price: dto.price,
        quantity: dto.quantity || 0,
        reorderLevel: dto.reorderLevel,
        categoryId: dto.categoryId,
        supplierId: dto.supplierId,
      },
      include: {
        category: true,
        supplier: true,
      },
    });
  }

  async update(id: number, dto: UpdateProductDto) {
    await this.findOne(id);

    if (dto.sku) {
      const existing = await this.prisma.product.findUnique({
        where: { sku: dto.sku.trim().toUpperCase() },
      });
      if (existing && existing.id !== id) {
        throw new ConflictException(`SKU '${dto.sku}' is already assigned to another product`);
      }
    }

    if (dto.categoryId) {
      const cat = await this.prisma.category.findUnique({ where: { id: dto.categoryId } });
      if (!cat) throw new NotFoundException(`Category ${dto.categoryId} not found`);
    }

    if (dto.supplierId) {
      const sup = await this.prisma.supplier.findUnique({ where: { id: dto.supplierId } });
      if (!sup) throw new NotFoundException(`Supplier ${dto.supplierId} not found`);
    }

    return this.prisma.product.update({
      where: { id },
      data: {
        ...(dto.sku && { sku: dto.sku.trim().toUpperCase() }),
        ...(dto.name && { name: dto.name.trim() }),
        ...(dto.price !== undefined && { price: dto.price }),
        ...(dto.reorderLevel !== undefined && { reorderLevel: dto.reorderLevel }),
        ...(dto.categoryId !== undefined && { categoryId: dto.categoryId }),
        ...(dto.supplierId !== undefined && { supplierId: dto.supplierId }),
      },
      include: {
        category: true,
        supplier: true,
      },
    });
  }

  async remove(id: number) {
    await this.findOne(id);
    const saleItemsCount = await this.prisma.saleItem.count({ where: { productId: id } });
    const purchaseItemsCount = await this.prisma.purchaseItem.count({ where: { productId: id } });

    if (saleItemsCount > 0 || purchaseItemsCount > 0) {
      throw new ConflictException('Cannot delete product with existing sales or purchase records');
    }

    return this.prisma.product.delete({ where: { id } });
  }
}

