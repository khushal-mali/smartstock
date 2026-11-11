import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ReportsService {
  constructor(private prisma: PrismaService) {}

  async getDashboardSummary() {
    const totalProducts = await this.prisma.product.count();
    const products = await this.prisma.product.findMany({
      include: {
        category: true,
        supplier: true,
      },
    });

    const lowStockProducts = products.filter((p) => p.quantity <= p.reorderLevel);

    const totalStockValue = products.reduce(
      (sum, p) => sum + Number(p.price) * p.quantity,
      0,
    );

    const totalSales = await this.prisma.sale.count();
    const sales = await this.prisma.sale.findMany({ select: { total: true } });
    const totalRevenue = sales.reduce((sum, s) => sum + Number(s.total), 0);

    const totalPurchases = await this.prisma.purchase.count();
    const purchases = await this.prisma.purchase.findMany({ select: { total: true } });
    const totalExpenses = purchases.reduce((sum, p) => sum + Number(p.total), 0);

    const recentSales = await this.prisma.sale.findMany({
      take: 5,
      orderBy: { date: 'desc' },
      include: {
        user: { select: { name: true } },
      },
    });

    return {
      totalProducts,
      lowStockCount: lowStockProducts.length,
      totalStockValue,
      totalSales,
      totalRevenue,
      totalPurchases,
      totalExpenses,
      lowStockAlerts: lowStockProducts.map((p) => ({
        id: p.id,
        sku: p.sku,
        name: p.name,
        quantity: p.quantity,
        reorderLevel: p.reorderLevel,
        category: p.category.name,
        supplier: p.supplier.name,
        supplierPhone: p.supplier.phone,
      })),
      recentSales,
    };
  }

  async getStockSummaryReport() {
    const products = await this.prisma.product.findMany({
      include: {
        category: true,
        supplier: true,
      },
      orderBy: { name: 'asc' },
    });

    return products.map((p) => ({
      id: p.id,
      sku: p.sku,
      name: p.name,
      category: p.category.name,
      supplier: p.supplier.name,
      price: Number(p.price),
      quantity: p.quantity,
      reorderLevel: p.reorderLevel,
      stockValue: Number(p.price) * p.quantity,
      isLowStock: p.quantity <= p.reorderLevel,
    }));
  }

  async getLowStockReport() {
    const products = await this.prisma.product.findMany({
      include: {
        category: true,
        supplier: true,
      },
      orderBy: { quantity: 'asc' },
    });

    return products
      .filter((p) => p.quantity <= p.reorderLevel)
      .map((p) => ({
        id: p.id,
        sku: p.sku,
        name: p.name,
        category: p.category.name,
        quantity: p.quantity,
        reorderLevel: p.reorderLevel,
        deficit: p.reorderLevel - p.quantity,
        supplierName: p.supplier.name,
        supplierPhone: p.supplier.phone,
        supplierEmail: p.supplier.email,
      }));
  }

  async getPurchasesReport(query?: { startDate?: string; endDate?: string; supplierId?: number }) {
    const where: any = {};

    if (query?.startDate || query?.endDate) {
      where.date = {};
      if (query.startDate) where.date.gte = new Date(query.startDate);
      if (query.endDate) {
        const end = new Date(query.endDate);
        end.setHours(23, 59, 59, 999);
        where.date.lte = end;
      }
    }

    if (query?.supplierId) {
      where.supplierId = Number(query.supplierId);
    }

    const purchases = await this.prisma.purchase.findMany({
      where,
      include: {
        supplier: true,
        user: { select: { name: true } },
        items: {
          include: {
            product: true,
          },
        },
      },
      orderBy: { date: 'desc' },
    });

    return purchases.map((p) => ({
      id: p.id,
      date: p.date,
      supplier: p.supplier.name,
      recordedBy: p.user.name,
      total: Number(p.total),
      itemCount: p.items.length,
      items: p.items.map((i) => ({
        productName: i.product.name,
        sku: i.product.sku,
        quantity: i.quantity,
        costPrice: Number(i.costPrice),
        subtotal: Number(i.costPrice) * i.quantity,
      })),
    }));
  }

  async getSalesReport(query?: { startDate?: string; endDate?: string }) {
    const where: any = {};

    if (query?.startDate || query?.endDate) {
      where.date = {};
      if (query.startDate) where.date.gte = new Date(query.startDate);
      if (query.endDate) {
        const end = new Date(query.endDate);
        end.setHours(23, 59, 59, 999);
        where.date.lte = end;
      }
    }

    const sales = await this.prisma.sale.findMany({
      where,
      include: {
        user: { select: { name: true } },
        items: {
          include: {
            product: true,
          },
        },
      },
      orderBy: { date: 'desc' },
    });

    return sales.map((s) => ({
      id: s.id,
      invoiceNo: s.invoiceNo,
      date: s.date,
      soldBy: s.user.name,
      total: Number(s.total),
      itemCount: s.items.length,
      items: s.items.map((i) => ({
        productName: i.product.name,
        sku: i.product.sku,
        quantity: i.quantity,
        price: Number(i.price),
        subtotal: Number(i.price) * i.quantity,
      })),
    }));
  }
}

