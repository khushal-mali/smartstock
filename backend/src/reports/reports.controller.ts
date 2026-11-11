import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { ReportsService } from './reports.service';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@UseGuards(JwtAuthGuard)
@Controller('reports')
export class ReportsController {
  constructor(private readonly reportsService: ReportsService) {}

  @Get('dashboard')
  getDashboardSummary() {
    return this.reportsService.getDashboardSummary();
  }

  @Get('stock-summary')
  getStockSummaryReport() {
    return this.reportsService.getStockSummaryReport();
  }

  @Get('low-stock')
  getLowStockReport() {
    return this.reportsService.getLowStockReport();
  }

  @Get('purchases')
  getPurchasesReport(
    @Query('startDate') startDate?: string,
    @Query('endDate') endDate?: string,
    @Query('supplierId') supplierId?: number,
  ) {
    return this.reportsService.getPurchasesReport({ startDate, endDate, supplierId });
  }

  @Get('sales')
  getSalesReport(
    @Query('startDate') startDate?: string,
    @Query('endDate') endDate?: string,
  ) {
    return this.reportsService.getSalesReport({ startDate, endDate });
  }
}

