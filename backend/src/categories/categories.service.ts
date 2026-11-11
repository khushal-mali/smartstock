import { Injectable, ConflictException, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateCategoryDto } from './dto/create-category.dto';

@Injectable()
export class CategoriesService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.category.findMany({
      include: {
        _count: {
          select: { products: true },
        },
      },
      orderBy: { name: 'asc' },
    });
  }

  async findOne(id: number) {
    const category = await this.prisma.category.findUnique({
      where: { id },
      include: { products: true },
    });
    if (!category) {
      throw new NotFoundException(`Category with ID ${id} not found`);
    }
    return category;
  }

  async create(dto: CreateCategoryDto) {
    const existing = await this.prisma.category.findUnique({
      where: { name: dto.name.trim() },
    });
    if (existing) {
      throw new ConflictException('Category with this name already exists');
    }
    return this.prisma.category.create({
      data: { name: dto.name.trim() },
    });
  }

  async update(id: number, dto: CreateCategoryDto) {
    await this.findOne(id);
    const existing = await this.prisma.category.findUnique({
      where: { name: dto.name.trim() },
    });
    if (existing && existing.id !== id) {
      throw new ConflictException('Category with this name already exists');
    }
    return this.prisma.category.update({
      where: { id },
      data: { name: dto.name.trim() },
    });
  }

  async remove(id: number) {
    await this.findOne(id);
    const count = await this.prisma.product.count({ where: { categoryId: id } });
    if (count > 0) {
      throw new ConflictException('Cannot delete category with associated products');
    }
    return this.prisma.category.delete({ where: { id } });
  }
}

