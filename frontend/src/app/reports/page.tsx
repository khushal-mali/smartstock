'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import {
  BarChart3,
  AlertTriangle,
  Package,
  ShoppingCart,
  Receipt,
  Printer,
  Calendar,
  Filter,
} from 'lucide-react';

export default function ReportsPage() {
  const [activeTab, setActiveTab] = useState<'stock' | 'low-stock' | 'purchases' | 'sales'>('stock');
  const [loading, setLoading] = useState(false);

  // Data states
  const [stockSummary, setStockSummary] = useState<any[]>([]);
  const [lowStockData, setLowStockData] = useState<any[]>([]);
  const [purchasesData, setPurchasesData] = useState<any[]>([]);
  const [salesData, setSalesData] = useState<any[]>([]);

  // Date filters for purchases & sales
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const fetchActiveReport = async () => {
    setLoading(true);
    try {
      if (activeTab === 'stock') {
        const res = await api.get('/reports/stock-summary');
        setStockSummary(res.data);
      } else if (activeTab === 'low-stock') {
        const res = await api.get('/reports/low-stock');
        setLowStockData(res.data);
      } else if (activeTab === 'purchases') {
        const params: any = {};
        if (startDate) params.startDate = startDate;
        if (endDate) params.endDate = endDate;
        const res = await api.get('/reports/purchases', { params });
        setPurchasesData(res.data);
      } else if (activeTab === 'sales') {
        const params: any = {};
        if (startDate) params.startDate = startDate;
        if (endDate) params.endDate = endDate;
        const res = await api.get('/reports/sales', { params });
        setSalesData(res.data);
      }
    } catch (err) {
      console.error('Failed to load report data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActiveReport();
  }, [activeTab]);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Header & Tabs */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4 print:hidden">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Reports Center</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Audit stock valuation, reorder thresholds, supplier purchases, and sales revenue
          </p>
        </div>

        <button
          onClick={handlePrint}
          className="flex items-center space-x-2 px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-xl text-xs font-semibold shadow-sm transition-all self-start md:self-auto"
        >
          <Printer className="h-4 w-4" />
          <span>Print / Export PDF</span>
        </button>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-200 gap-2 print:hidden overflow-x-auto">
        <button
          onClick={() => setActiveTab('stock')}
          className={`flex items-center space-x-2 py-3 px-4 border-b-2 font-semibold text-xs transition-all whitespace-nowrap ${
            activeTab === 'stock'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Package className="h-4 w-4" />
          <span>1. Stock Summary</span>
        </button>
        <button
          onClick={() => setActiveTab('low-stock')}
          className={`flex items-center space-x-2 py-3 px-4 border-b-2 font-semibold text-xs transition-all whitespace-nowrap ${
            activeTab === 'low-stock'
              ? 'border-rose-600 text-rose-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <AlertTriangle className="h-4 w-4" />
          <span>2. Low-Stock Report</span>
        </button>
        <button
          onClick={() => setActiveTab('purchases')}
          className={`flex items-center space-x-2 py-3 px-4 border-b-2 font-semibold text-xs transition-all whitespace-nowrap ${
            activeTab === 'purchases'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <ShoppingCart className="h-4 w-4" />
          <span>3. Purchase Report</span>
        </button>
        <button
          onClick={() => setActiveTab('sales')}
          className={`flex items-center space-x-2 py-3 px-4 border-b-2 font-semibold text-xs transition-all whitespace-nowrap ${
            activeTab === 'sales'
              ? 'border-emerald-600 text-emerald-600'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Receipt className="h-4 w-4" />
          <span>4. Sales Report</span>
        </button>
      </div>

      {/* Date Range Filter for Purchases and Sales */}
      {(activeTab === 'purchases' || activeTab === 'sales') && (
        <div className="bg-white p-4 rounded-xl border border-slate-200 flex flex-wrap items-center gap-3 print:hidden">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-600">
            <Calendar className="h-4 w-4 text-slate-400" />
            <span>Date Range:</span>
          </div>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
          />
          <span className="text-slate-400 text-xs">to</span>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
          />
          <button
            onClick={fetchActiveReport}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-medium"
          >
            Apply Filter
          </button>
          {(startDate || endDate) && (
            <button
              onClick={() => {
                setStartDate('');
                setEndDate('');
                setTimeout(fetchActiveReport, 50);
              }}
              className="text-xs text-slate-500 hover:text-slate-700 underline"
            >
              Reset
            </button>
          )}
        </div>
      )}

      {/* Print Document Header (Visible only when printing) */}
      <div className="hidden print:block mb-6">
        <h1 className="text-2xl font-black text-slate-900">SmartStock – Official Audit Report</h1>
        <p className="text-sm text-slate-600">
          Report Type: {activeTab.toUpperCase()} | Generated on: {new Date().toLocaleDateString('en-IN')}
        </p>
      </div>

      {/* Report Table Content */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center">
            <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          </div>
        ) : (
          <>
            {/* 1. STOCK SUMMARY */}
            {activeTab === 'stock' && (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                    <tr>
                      <th className="py-3 px-4">Product Name</th>
                      <th className="py-3 px-4">SKU</th>
                      <th className="py-3 px-4">Category</th>
                      <th className="py-3 px-4">Supplier</th>
                      <th className="py-3 px-4 text-center">Stock Qty</th>
                      <th className="py-3 px-4 text-right">Unit Price</th>
                      <th className="py-3 px-4 text-right">Total Valuation</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {stockSummary.map((item) => (
                      <tr key={item.id} className="hover:bg-slate-50/60">
                        <td className="py-3 px-4 font-semibold text-slate-900">{item.name}</td>
                        <td className="py-3 px-4 font-mono text-xs text-slate-500">{item.sku}</td>
                        <td className="py-3 px-4 text-slate-600">{item.category}</td>
                        <td className="py-3 px-4 text-slate-600">{item.supplier}</td>
                        <td className="py-3 px-4 text-center font-bold text-slate-800">
                          {item.quantity}
                          {item.isLowStock && (
                            <span className="ml-2 text-[10px] px-1.5 py-0.5 rounded bg-rose-100 text-rose-700 font-bold">
                              LOW
                            </span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-right text-slate-700">
                          ₹{item.price.toFixed(2)}
                        </td>
                        <td className="py-3 px-4 text-right font-black text-slate-900">
                          ₹{item.stockValue.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot className="bg-slate-50 font-bold text-slate-900 border-t border-slate-200">
                    <tr>
                      <td colSpan={6} className="py-3 px-4 text-right uppercase text-xs">
                        Total Inventory Valuation:
                      </td>
                      <td className="py-3 px-4 text-right text-base font-black text-emerald-600">
                        ₹
                        {stockSummary
                          .reduce((sum, i) => sum + i.stockValue, 0)
                          .toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            )}

            {/* 2. LOW-STOCK REPORT */}
            {activeTab === 'low-stock' && (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-rose-50/50 text-xs font-semibold text-rose-700 uppercase tracking-wider border-b border-rose-100">
                    <tr>
                      <th className="py-3 px-4">Item Name</th>
                      <th className="py-3 px-4">SKU</th>
                      <th className="py-3 px-4">Category</th>
                      <th className="py-3 px-4 text-center">Current Qty</th>
                      <th className="py-3 px-4 text-center">Reorder Threshold</th>
                      <th className="py-3 px-4 text-center">Shortage Deficit</th>
                      <th className="py-3 px-4">Preferred Supplier</th>
                      <th className="py-3 px-4">Contact Details</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {lowStockData.length > 0 ? (
                      lowStockData.map((item) => (
                        <tr key={item.id} className="hover:bg-rose-50/30">
                          <td className="py-3 px-4 font-semibold text-slate-900">{item.name}</td>
                          <td className="py-3 px-4 font-mono text-xs text-slate-500">{item.sku}</td>
                          <td className="py-3 px-4 text-slate-600">{item.category}</td>
                          <td className="py-3 px-4 text-center font-bold text-rose-600">
                            {item.quantity} units
                          </td>
                          <td className="py-3 px-4 text-center text-slate-600">
                            {item.reorderLevel} units
                          </td>
                          <td className="py-3 px-4 text-center font-black text-rose-700">
                            -{item.deficit} units
                          </td>
                          <td className="py-3 px-4 font-medium text-slate-800">{item.supplierName}</td>
                          <td className="py-3 px-4 text-xs text-slate-500">
                            <div>{item.supplierPhone}</div>
                            <div>{item.supplierEmail}</div>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={8} className="p-8 text-center text-slate-400">
                          No low-stock items detected!
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}

            {/* 3. PURCHASES REPORT */}
            {activeTab === 'purchases' && (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                    <tr>
                      <th className="py-3 px-4">PO Ref</th>
                      <th className="py-3 px-4">Date</th>
                      <th className="py-3 px-4">Supplier</th>
                      <th className="py-3 px-4">Recorded By</th>
                      <th className="py-3 px-4">Items Summary</th>
                      <th className="py-3 px-4 text-right">Order Total</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {purchasesData.length > 0 ? (
                      purchasesData.map((item) => (
                        <tr key={item.id} className="hover:bg-slate-50/60">
                          <td className="py-3 px-4 font-mono font-bold text-blue-600">PO #{item.id}</td>
                          <td className="py-3 px-4 text-slate-600">
                            {new Date(item.date).toLocaleDateString('en-IN')}
                          </td>
                          <td className="py-3 px-4 font-medium text-slate-900">{item.supplier}</td>
                          <td className="py-3 px-4 text-slate-600">{item.recordedBy}</td>
                          <td className="py-3 px-4 text-xs text-slate-600">
                            {item.items.map((it: any, idx: number) => (
                              <span key={idx} className="mr-2">
                                {it.productName} ({it.quantity} @ ₹{it.costPrice})
                              </span>
                            ))}
                          </td>
                          <td className="py-3 px-4 text-right font-black text-slate-900">
                            ₹{item.total.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={6} className="p-8 text-center text-slate-400">
                          No purchase records match this range.
                        </td>
                      </tr>
                    )}
                  </tbody>
                  {purchasesData.length > 0 && (
                    <tfoot className="bg-slate-50 font-bold text-slate-900 border-t border-slate-200">
                      <tr>
                        <td colSpan={5} className="py-3 px-4 text-right uppercase text-xs">
                          Total Procurement Expenditure:
                        </td>
                        <td className="py-3 px-4 text-right text-base font-black text-blue-600">
                          ₹
                          {purchasesData
                            .reduce((sum, p) => sum + p.total, 0)
                            .toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                        </td>
                      </tr>
                    </tfoot>
                  )}
                </table>
              </div>
            )}

            {/* 4. SALES REPORT */}
            {activeTab === 'sales' && (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                    <tr>
                      <th className="py-3 px-4">Invoice No</th>
                      <th className="py-3 px-4">Date</th>
                      <th className="py-3 px-4">Sold By</th>
                      <th className="py-3 px-4">Item Details</th>
                      <th className="py-3 px-4 text-right">Revenue</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {salesData.length > 0 ? (
                      salesData.map((item) => (
                        <tr key={item.id} className="hover:bg-slate-50/60">
                          <td className="py-3 px-4 font-mono font-bold text-blue-600">{item.invoiceNo}</td>
                          <td className="py-3 px-4 text-slate-600">
                            {new Date(item.date).toLocaleDateString('en-IN')}
                          </td>
                          <td className="py-3 px-4 text-slate-700">{item.soldBy}</td>
                          <td className="py-3 px-4 text-xs text-slate-600">
                            {item.items.map((it: any, idx: number) => (
                              <span key={idx} className="mr-2">
                                {it.productName} ({it.quantity} × ₹{it.price})
                              </span>
                            ))}
                          </td>
                          <td className="py-3 px-4 text-right font-black text-emerald-600">
                            ₹{item.total.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={5} className="p-8 text-center text-slate-400">
                          No sales found in this range.
                        </td>
                      </tr>
                    )}
                  </tbody>
                  {salesData.length > 0 && (
                    <tfoot className="bg-slate-50 font-bold text-slate-900 border-t border-slate-200">
                      <tr>
                        <td colSpan={4} className="py-3 px-4 text-right uppercase text-xs">
                          Total Realized Sales Revenue:
                        </td>
                        <td className="py-3 px-4 text-right text-base font-black text-emerald-600">
                          ₹
                          {salesData
                            .reduce((sum, s) => sum + s.total, 0)
                            .toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                        </td>
                      </tr>
                    </tfoot>
                  )}
                </table>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

