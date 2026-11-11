'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import api from '@/lib/api';
import {
  Package,
  AlertTriangle,
  DollarSign,
  TrendingUp,
  ShoppingCart,
  Receipt,
  ArrowUpRight,
  PlusCircle,
  Truck,
  Phone,
} from 'lucide-react';

interface DashboardData {
  totalProducts: number;
  lowStockCount: number;
  totalStockValue: number;
  totalSales: number;
  totalRevenue: number;
  totalPurchases: number;
  totalExpenses: number;
  lowStockAlerts: {
    id: number;
    sku: string;
    name: string;
    quantity: number;
    reorderLevel: number;
    category: string;
    supplier: string;
    supplierPhone: string;
  }[];
  recentSales: {
    id: number;
    invoiceNo: string;
    date: string;
    total: number;
    user: { name: string };
  }[];
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboard = async () => {
    try {
      const res = await api.get('/reports/dashboard');
      setData(res.data);
    } catch (err) {
      console.error('Failed to fetch dashboard data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner & Quick Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Inventory Overview</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time stock indicators, valuation, and threshold reorder alerts
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Link
            href="/sales"
            className="flex items-center space-x-1.5 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-semibold shadow-sm transition-all"
          >
            <Receipt className="h-4 w-4" />
            <span>New Sale (POS)</span>
          </Link>
          <Link
            href="/purchases"
            className="flex items-center space-x-1.5 px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold shadow-sm transition-all"
          >
            <ShoppingCart className="h-4 w-4" />
            <span>Record Purchase</span>
          </Link>
          <Link
            href="/products"
            className="flex items-center space-x-1.5 px-3.5 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-xl text-xs font-semibold shadow-sm transition-all"
          >
            <PlusCircle className="h-4 w-4" />
            <span>Manage Products</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Products */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Products</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">{data?.totalProducts || 0}</h3>
            <p className="text-[11px] text-slate-400 mt-1">Catalog items</p>
          </div>
          <div className="h-12 w-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
            <Package className="h-6 w-6" />
          </div>
        </div>

        {/* Low Stock Alerts */}
        <div className="bg-white p-5 rounded-2xl border border-rose-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-rose-600 uppercase tracking-wider">Low Stock Alerts</p>
            <h3 className="text-2xl font-black text-rose-600 mt-1">{data?.lowStockCount || 0}</h3>
            <p className="text-[11px] text-rose-500 font-medium mt-1">Requires reorder</p>
          </div>
          <div className="h-12 w-12 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
            <AlertTriangle className="h-6 w-6" />
          </div>
        </div>

        {/* Total Inventory Value */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Inventory Value</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">
              ₹{(data?.totalStockValue || 0).toLocaleString('en-IN')}
            </h3>
            <p className="text-[11px] text-emerald-600 font-medium mt-1">Active valuation</p>
          </div>
          <div className="h-12 w-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <DollarSign className="h-6 w-6" />
          </div>
        </div>

        {/* Total Revenue */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Sales Revenue</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">
              ₹{(data?.totalRevenue || 0).toLocaleString('en-IN')}
            </h3>
            <p className="text-[11px] text-slate-400 mt-1">{data?.totalSales || 0} sales recorded</p>
          </div>
          <div className="h-12 w-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
            <TrendingUp className="h-6 w-6" />
          </div>
        </div>
      </div>

      {/* Critical Low-Stock Warning Section */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="h-3 w-3 rounded-full bg-rose-500 animate-ping"></div>
            <h3 className="text-base font-bold text-slate-900">
              Low Stock Warnings ({data?.lowStockAlerts?.length || 0})
            </h3>
          </div>
          <Link
            href="/reports"
            className="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center space-x-1"
          >
            <span>View Full Report</span>
            <ArrowUpRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        {data?.lowStockAlerts && data.lowStockAlerts.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Product Name</th>
                  <th className="py-3 px-4">SKU</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Current Stock</th>
                  <th className="py-3 px-4">Reorder Level</th>
                  <th className="py-3 px-4">Supplier</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {data.lowStockAlerts.map((item) => (
                  <tr key={item.id} className="hover:bg-rose-50/30 transition-colors">
                    <td className="py-3 px-4 font-semibold text-slate-900">{item.name}</td>
                    <td className="py-3 px-4 font-mono text-xs text-slate-500">{item.sku}</td>
                    <td className="py-3 px-4 text-slate-600">{item.category}</td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-700">
                        {item.quantity} units
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-600">{item.reorderLevel} units</td>
                    <td className="py-3 px-4 text-slate-700 font-medium">
                      <div className="flex items-center space-x-1.5">
                        <Truck className="h-3.5 w-3.5 text-slate-400" />
                        <span>{item.supplier}</span>
                      </div>
                      <div className="flex items-center space-x-1 text-[11px] text-slate-400 mt-0.5">
                        <Phone className="h-3 w-3" />
                        <span>{item.supplierPhone}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <Link
                        href={`/purchases?productId=${item.id}&supplier=${encodeURIComponent(item.supplier)}`}
                        className="inline-flex items-center space-x-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-medium shadow-sm transition-colors"
                      >
                        <ShoppingCart className="h-3.5 w-3.5" />
                        <span>Reorder</span>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center text-slate-400 text-sm">
            All inventory levels are healthy! No items are currently at or below reorder levels.
          </div>
        )}
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-base font-bold text-slate-900">Recent Sales Invoices</h3>
          <Link
            href="/sales"
            className="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center space-x-1"
          >
            <span>View Billing History</span>
            <ArrowUpRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        {data?.recentSales && data.recentSales.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Invoice No</th>
                  <th className="py-3 px-4">Date</th>
                  <th className="py-3 px-4">Cashier / Staff</th>
                  <th className="py-3 px-4 text-right">Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {data.recentSales.map((sale) => (
                  <tr key={sale.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3 px-4 font-mono font-semibold text-blue-600">{sale.invoiceNo}</td>
                    <td className="py-3 px-4 text-slate-600">
                      {new Date(sale.date).toLocaleDateString('en-IN', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </td>
                    <td className="py-3 px-4 text-slate-700">{sale.user.name}</td>
                    <td className="py-3 px-4 font-bold text-slate-900 text-right">
                      ₹{Number(sale.total).toLocaleString('en-IN')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center text-slate-400 text-sm">No sales recorded yet.</div>
        )}
      </div>
    </div>
  );
}
