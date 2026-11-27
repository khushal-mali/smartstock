import { Test, TestingModule } from '@nestjs/testing';
import { ReportsService } from './reports.service';
import { PrismaService } from '../prisma/prisma.service';

describe('ReportsService (Unit Tests)', () => {
  let service: ReportsService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ReportsService,
        {
          provide: PrismaService,
          useValue: {
            product: {
              count: jest.fn().mockResolvedValue(3),
              findMany: jest.fn().mockResolvedValue([
                {
                  id: 1,
                  sku: 'P1',
                  name: 'Healthy Stock Item',
                  price: 100,
                  quantity: 50,
                  reorderLevel: 10,
                  category: { name: 'Cat A' },
                  supplier: { name: 'Sup A', phone: '123' },
                },
                {
                  id: 2,
                  sku: 'P2',
                  name: 'Low Stock Item',
                  price: 200,
                  quantity: 4, // 4 <= 10 -> Low stock
                  reorderLevel: 10,
                  category: { name: 'Cat B' },
                  supplier: { name: 'Sup B', phone: '456' },
                },
              ]),
            },
            sale: {
              count: jest.fn().mockResolvedValue(10),
              findMany: jest.fn().mockResolvedValue([{ total: 1500 }, { total: 3500 }]),
            },
            purchase: {
              count: jest.fn().mockResolvedValue(5),
              findMany: jest.fn().mockResolvedValue([{ total: 10000 }]),
            },
          },
        },
      ],
    }).compile();

    service = module.get<ReportsService>(ReportsService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should compute total inventory valuation and detect low stock count correctly', async () => {
    const summary = await service.getDashboardSummary();
    expect(summary.totalProducts).toBe(3);
    expect(summary.lowStockCount).toBe(1);
    expect(summary.totalStockValue).toBe(50 * 100 + 4 * 200); // 5000 + 800 = 5800
    expect(summary.totalRevenue).toBe(5000);
    expect(summary.totalExpenses).toBe(10000);
  });

  it('should generate low-stock items with deficit and supplier details', async () => {
    const lowStock = await service.getLowStockReport();
    expect(lowStock).toHaveLength(1);
    expect(lowStock[0].name).toBe('Low Stock Item');
    expect(lowStock[0].deficit).toBe(6); // 10 - 4 = 6
    expect(lowStock[0].supplierName).toBe('Sup B');
  });
});

