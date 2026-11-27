import { Test, TestingModule } from '@nestjs/testing';
import { SalesService } from './sales.service';
import { PrismaService } from '../prisma/prisma.service';
import { BadRequestException, NotFoundException } from '@nestjs/common';

describe('SalesService (Unit & Transaction Tests)', () => {
  let service: SalesService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        SalesService,
        {
          provide: PrismaService,
          useValue: {
            sale: {
              findMany: jest.fn(),
              findUnique: jest.fn(),
              count: jest.fn().mockResolvedValue(4),
            },
            product: {
              findUnique: jest.fn(),
            },
            $transaction: jest.fn((cb) =>
              cb({
                sale: {
                  create: jest.fn().mockResolvedValue({
                    id: 5,
                    invoiceNo: 'INV-202611-0005',
                    userId: 1,
                    total: 1700,
                    user: { name: 'Cashier' },
                    items: [],
                  }),
                },
                product: {
                  update: jest.fn().mockResolvedValue({}),
                },
              }),
            ),
          },
        },
      ],
    }).compile();

    service = module.get<SalesService>(SalesService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should block sale if requested quantity exceeds available stock', async () => {
    jest.spyOn(prisma.product, 'findUnique').mockResolvedValue({
      id: 10,
      name: 'Wireless Mouse',
      sku: 'ELEC-MOU-01',
      quantity: 5,
      price: 500,
    } as any);

    await expect(
      service.create(1, {
        items: [{ productId: 10, quantity: 12 }], // 12 requested, only 5 available
      }),
    ).rejects.toThrow(BadRequestException);
  });

  it('should throw NotFoundException if product ID is invalid', async () => {
    jest.spyOn(prisma.product, 'findUnique').mockResolvedValue(null);

    await expect(
      service.create(1, {
        items: [{ productId: 999, quantity: 1 }],
      }),
    ).rejects.toThrow(NotFoundException);
  });

  it('should process sale and assign sequential invoice number within transaction', async () => {
    jest.spyOn(prisma.product, 'findUnique').mockResolvedValue({
      id: 1,
      name: 'Keyboard',
      sku: 'ELEC-KB-01',
      quantity: 20,
      price: 850,
    } as any);

    const result = await service.create(1, {
      items: [{ productId: 1, quantity: 2 }],
    });

    expect(result).toHaveProperty('invoiceNo', 'INV-202611-0005');
    expect(prisma.$transaction).toHaveBeenCalled();
  });
});

