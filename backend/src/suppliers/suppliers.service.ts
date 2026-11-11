import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateSupplierDto } from './dto/create-supplier.dto';

@Injectable()
export class SuppliersService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.supplier.findMany({
      include: {
        _count: {
          select: { products: true, purchases: true },
        },
      },
      orderBy: { name: 'asc' },
    });
  }

  async findOne(id: number) {
    const supplier = await this.prisma.supplier.findUnique({
      where: { id },
      include: {
        products: true,
        purchases: {
          orderBy: { date: 'desc' },
          take: 5,
        },
      },
    });
    if (!supplier) {
      throw new NotFoundException(`Supplier with ID ${id} not found`);
    }
    return supplier;
  }

  async create(dto: CreateSupplierDto) {
    return this.prisma.supplier.create({
      data: {
        name: dto.name.trim(),
        phone: dto.phone.trim(),
        email: dto.email.trim().toLowerCase(),
      },
    });
  }

  async update(id: number, dto: CreateSupplierDto) {
    await this.findOne(id);
    return this.prisma.supplier.update({
      where: { id },
      data: {
        name: dto.name.trim(),
        phone: dto.phone.trim(),
        email: dto.email.trim().toLowerCase(),
      },
    });
  }

  async remove(id: number) {
    await this.findOne(id);
    const count = await this.prisma.product.count({ where: { supplierId: id } });
    if (count > 0) {
      throw new ConflictException('Cannot delete supplier with linked products');
    }
    return this.prisma.supplier.delete({ where: { id } });
  }
}

