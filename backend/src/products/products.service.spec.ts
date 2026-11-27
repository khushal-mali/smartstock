import { Test, TestingModule } from '@nestjs/testing';
import { ProductsService } from './products.service';
import { PrismaService } from '../prisma/prisma.service';
import { ConflictException, NotFoundException } from '@nestjs/common';

describe('ProductsService (Unit Tests)', () => {
  let service: ProductsService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ProductsService,
        {
          provide: PrismaService,
          useValue: {
            product: {
              findMany: jest.fn(),
              findUnique: jest.fn(),
              create: jest.fn(),
              update: jest.fn(),
              delete: jest.fn(),
              count: jest.fn(),
            },
            category: {
              findUnique: jest.fn(),
            },
            supplier: {
              findUnique: jest.fn(),
            },
          },
        },
      ],
    }).compile();

    service = module.get<ProductsService>(ProductsService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should throw ConflictException if SKU already exists', async () => {
    jest.spyOn(prisma.product, 'findUnique').mockResolvedValue({
      id: 1,
      sku: 'SKU-EXISTING',
    } as any);

    await expect(
      service.create({
        sku: 'SKU-EXISTING',
        name: 'Duplicate Product',
        price: 500,
        reorderLevel: 5,
        categoryId: 1,
        supplierId: 1,
      }),
    ).rejects.toThrow(ConflictException);
  });

  it('should filter low-stock products correctly where quantity <= reorderLevel', async () => {
    jest.spyOn(prisma.product, 'findMany').mockResolvedValue([
      { id: 1, name: 'Prod A', quantity: 15, reorderLevel: 10 },
      { id: 2, name: 'Prod B', quantity: 3, reorderLevel: 5 }, // Low stock
    ] as any);

    const result = await service.findAll({ lowStock: true });
    expect(result).toHaveLength(1);
    expect(result[0].name).toBe('Prod B');
  });
});

