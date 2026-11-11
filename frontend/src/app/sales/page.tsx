'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import {
  Receipt,
  Plus,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  Printer,
  X,
  Package,
  History,
  FileText,
} from 'lucide-react';

interface Product {
  id: number;
  name: string;
  sku: string;
  quantity: number;
  price: number;
}

interface SaleRow {
  productId: number;
  quantity: number;
  price: number;
}

interface CompletedSale {
  id: number;
  invoiceNo: string;
  date: string;
  total: number;
  user: { name: string };
  items: {
    id: number;
    quantity: number;
    price: number;
    product: { name: string; sku: string };
  }[];
}

export default function SalesBillingPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [history, setHistory] = useState<CompletedSale[]>([]);
  const [loading, setLoading] = useState(true);

  // Billing Rows
  const [rows, setRows] = useState<SaleRow[]>([{ productId: 0, quantity: 1, price: 0 }]);
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  // Invoice Modal
  const [activeInvoice, setActiveInvoice] = useState<CompletedSale | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [prodRes, histRes] = await Promise.all([api.get('/products'), api.get('/sales')]);
      setProducts(prodRes.data);
      setHistory(histRes.data);
      if (prodRes.data.length > 0) {
        setRows([{ productId: prodRes.data[0].id, quantity: 1, price: Number(prodRes.data[0].price) }]);
      }
    } catch (err) {
      console.error('Failed to load billing data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const addRow = () => {
    const firstProd = products[0];
    setRows([
      ...rows,
      {
        productId: firstProd ? firstProd.id : 0,
        quantity: 1,
        price: firstProd ? Number(firstProd.price) : 0,
      },
    ]);
  };

  const removeRow = (index: number) => {
    if (rows.length === 1) return;
    setRows(rows.filter((_, i) => i !== index));
  };

  const updateRow = (index: number, field: keyof SaleRow, val: any) => {
    const updated = [...rows];
    if (field === 'productId') {
      const selected = products.find((p) => p.id === Number(val));
      updated[index].productId = Number(val);
      if (selected) {
        updated[index].price = Number(selected.price);
      }
    } else {
      updated[index][field] = Number(val);
    }
    setRows(updated);
  };

  const calculateGrandTotal = () => {
    return rows.reduce((sum, r) => sum + r.quantity * (r.price || 0), 0);
  };

  const handleCheckout = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSubmitting(true);

    try {
      // Validate in-memory stock limits before sending
      for (const row of rows) {
        const prod = products.find((p) => p.id === row.productId);
        if (!prod) throw new Error('Please select a valid product for each row');
        if (row.quantity > prod.quantity) {
          throw new Error(
            `Cannot sell ${row.quantity} units of '${prod.name}'. Only ${prod.quantity} available in stock!`,
          );
        }
      }

      const res = await api.post('/sales', {
        items: rows.map((r) => ({
          productId: Number(r.productId),
          quantity: Number(r.quantity),
          price: Number(r.price),
        })),
      });

      // Show Invoice Modal
      setActiveInvoice(res.data);

      // Refresh product quantities and history
      loadData();
    } catch (err: any) {
      setErrorMsg(err.response?.data?.message || err.message || 'Failed to process sale');
    } finally {
      setSubmitting(false);
    }
  };

  const printInvoice = () => {
    window.print();
  };

  return (
    <div className="space-y-8 max-w-5xl">
      {/* Billing POS Interface */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center space-x-3 pb-4 border-b border-slate-100">
          <div className="h-10 w-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <Receipt className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">Billing Counter & POS</h2>
            <p className="text-xs text-slate-500">
              Generate sales invoices with automated stock deduction and quantity validation
            </p>
          </div>
        </div>

        {errorMsg && (
          <div className="mt-4 p-3 rounded-xl bg-rose-50 border border-rose-200 flex items-center space-x-2 text-rose-700 text-xs font-semibold">
            <AlertTriangle className="h-4 w-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleCheckout} className="mt-6 space-y-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Cart Items
              </label>
              <button
                type="button"
                onClick={addRow}
                className="flex items-center space-x-1 text-xs font-semibold text-blue-600 hover:text-blue-700"
              >
                <Plus className="h-3.5 w-3.5" />
                <span>Add Item</span>
              </button>
            </div>

            {rows.map((row, idx) => {
              const selectedProd = products.find((p) => p.id === row.productId);
              const isShort = selectedProd && row.quantity > selectedProd.quantity;

              return (
                <div
                  key={idx}
                  className={`flex flex-wrap sm:flex-nowrap items-center gap-3 p-3 rounded-xl border transition-colors ${
                    isShort ? 'bg-rose-50/50 border-rose-300' : 'bg-slate-50 border-slate-200'
                  }`}
                >
                  <div className="flex-1 min-w-[220px]">
                    <span className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                      Product & Stock
                    </span>
                    <select
                      required
                      value={row.productId}
                      onChange={(e) => updateRow(idx, 'productId', e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-800 focus:ring-2 focus:ring-blue-500"
                    >
                      {products.map((p) => (
                        <option key={p.id} value={p.id} disabled={p.quantity <= 0}>
                          {p.name} ({p.sku}) — Available: {p.quantity} units {p.quantity <= 0 ? '(OUT OF STOCK)' : ''}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="w-28">
                    <span className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                      Qty
                    </span>
                    <input
                      type="number"
                      min="1"
                      required
                      value={row.quantity}
                      onChange={(e) => updateRow(idx, 'quantity', e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-center font-bold text-slate-800 focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div className="w-32">
                    <span className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                      Unit Price (₹)
                    </span>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      required
                      value={row.price}
                      onChange={(e) => updateRow(idx, 'price', e.target.value)}
                      className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm font-mono text-slate-800 focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div className="w-32 text-right">
                    <span className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                      Subtotal
                    </span>
                    <p className="py-2 text-sm font-bold text-slate-900">
                      ₹{(row.quantity * (row.price || 0)).toLocaleString('en-IN')}
                    </p>
                  </div>

                  <div className="pt-4">
                    <button
                      type="button"
                      onClick={() => removeRow(idx)}
                      disabled={rows.length === 1}
                      className="p-2 text-rose-500 hover:bg-rose-50 rounded-lg disabled:opacity-30 transition-colors"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Grand Total & Checkout */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
            <div>
              <p className="text-xs text-slate-500">Bill Grand Total</p>
              <h3 className="text-3xl font-black text-emerald-600">
                ₹{calculateGrandTotal().toLocaleString('en-IN')}
              </h3>
            </div>
            <button
              type="submit"
              disabled={submitting}
              className="w-full sm:w-auto px-8 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm rounded-xl shadow-lg shadow-emerald-600/20 transition-all disabled:opacity-50 flex items-center justify-center space-x-2"
            >
              <Receipt className="h-4 w-4" />
              <span>{submitting ? 'Generating Invoice...' : 'Generate Bill & Complete Sale'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Invoice History */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-5 border-b border-slate-100 flex items-center space-x-2">
          <History className="h-5 w-5 text-slate-400" />
          <h3 className="text-base font-bold text-slate-900">Recent Sales Invoices</h3>
        </div>

        {history.length > 0 ? (
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Invoice No</th>
                <th className="py-3 px-4">Date</th>
                <th className="py-3 px-4">Staff Member</th>
                <th className="py-3 px-4">Items Sold</th>
                <th className="py-3 px-4">Total Amount</th>
                <th className="py-3 px-4 text-right">View / Print</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {history.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3 px-4 font-mono font-bold text-blue-600">{s.invoiceNo}</td>
                  <td className="py-3 px-4 text-slate-600">
                    {new Date(s.date).toLocaleDateString('en-IN', {
                      day: '2-digit',
                      month: 'short',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </td>
                  <td className="py-3 px-4 text-slate-700">{s.user.name}</td>
                  <td className="py-3 px-4 text-slate-600">{s.items.length} items</td>
                  <td className="py-3 px-4 font-bold text-slate-900">
                    ₹{Number(s.total).toLocaleString('en-IN')}
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => setActiveInvoice(s)}
                      className="inline-flex items-center space-x-1 px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-medium transition-colors"
                    >
                      <FileText className="h-3.5 w-3.5" />
                      <span>Invoice</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="p-12 text-center text-slate-400 text-sm">No sales records found.</div>
        )}
      </div>

      {/* Printable Invoice Modal */}
      {activeInvoice && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-xl w-full p-8 shadow-2xl border border-slate-200 max-h-[90vh] overflow-y-auto">
            {/* Modal Header Controls (Hidden on print) */}
            <div className="flex items-center justify-between pb-4 border-b border-slate-100 print:hidden">
              <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">
                Sale Completed
              </span>
              <div className="flex items-center space-x-2">
                <button
                  onClick={printInvoice}
                  className="flex items-center space-x-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold shadow-sm"
                >
                  <Printer className="h-3.5 w-3.5" />
                  <span>Print Tax Invoice</span>
                </button>
                <button
                  onClick={() => setActiveInvoice(null)}
                  className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Printable Tax Invoice Document */}
            <div className="mt-4 space-y-6">
              {/* Company & Invoice Header */}
              <div className="flex items-start justify-between">
                <div>
                  <h1 className="text-2xl font-black text-slate-900">SmartStock Retail</h1>
                  <p className="text-xs text-slate-500 mt-0.5">Inventory & Retail Store</p>
                  <p className="text-xs text-slate-400">Dehradun, Uttarakhand, India</p>
                </div>
                <div className="text-right">
                  <span className="inline-block px-2.5 py-1 bg-slate-100 rounded text-xs font-mono font-bold text-slate-800">
                    {activeInvoice.invoiceNo}
                  </span>
                  <p className="text-xs text-slate-500 mt-1">
                    Date:{' '}
                    {new Date(activeInvoice.date).toLocaleDateString('en-IN', {
                      day: '2-digit',
                      month: 'short',
                      year: 'numeric',
                    })}
                  </p>
                  <p className="text-xs text-slate-500">Billed by: {activeInvoice.user.name}</p>
                </div>
              </div>

              {/* Items Table */}
              <table className="w-full text-left text-xs border border-slate-200 rounded-lg overflow-hidden">
                <thead className="bg-slate-50 font-semibold text-slate-700 border-b border-slate-200">
                  <tr>
                    <th className="py-2.5 px-3">Item Description</th>
                    <th className="py-2.5 px-3">SKU</th>
                    <th className="py-2.5 px-3 text-center">Qty</th>
                    <th className="py-2.5 px-3 text-right">Rate (₹)</th>
                    <th className="py-2.5 px-3 text-right">Amount (₹)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {activeInvoice.items.map((it, i) => (
                    <tr key={i}>
                      <td className="py-2.5 px-3 font-medium text-slate-900">{it.product.name}</td>
                      <td className="py-2.5 px-3 font-mono text-slate-500">{it.product.sku}</td>
                      <td className="py-2.5 px-3 text-center font-bold text-slate-800">{it.quantity}</td>
                      <td className="py-2.5 px-3 text-right text-slate-600">
                        {Number(it.price).toFixed(2)}
                      </td>
                      <td className="py-2.5 px-3 text-right font-bold text-slate-900">
                        {(it.quantity * Number(it.price)).toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Total Summary */}
              <div className="flex justify-end pt-2">
                <div className="w-48 space-y-1.5 text-xs text-right">
                  <div className="flex justify-between text-slate-500">
                    <span>Subtotal:</span>
                    <span>₹{Number(activeInvoice.total).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-slate-500">
                    <span>Taxes (GST 0%):</span>
                    <span>₹0.00</span>
                  </div>
                  <div className="flex justify-between text-base font-black text-slate-900 pt-2 border-t border-slate-200">
                    <span>Grand Total:</span>
                    <span>₹{Number(activeInvoice.total).toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {/* Footer Note */}
              <div className="text-center pt-6 border-t border-slate-100 text-[11px] text-slate-400">
                Thank you for your business! SmartStock Inventory System.
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

