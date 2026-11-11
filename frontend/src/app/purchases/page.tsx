'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { ShoppingCart, Plus, Trash2, CheckCircle2, AlertCircle, History, Package, Truck } from 'lucide-react';

interface Supplier {
  id: number;
  name: string;
}

interface Product {
  id: number;
  name: string;
  sku: string;
  quantity: number;
  price: number;
}

interface PurchaseItemRow {
  productId: number;
  quantity: number;
  costPrice: number;
}

interface PurchaseHistory {
  id: number;
  date: string;
  total: number;
  supplier: { name: string };
  user: { name: string };
  items: {
    id: number;
    quantity: number;
    costPrice: number;
    product: { name: string; sku: string };
  }[];
}

export default function PurchasesPage() {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [history, setHistory] = useState<PurchaseHistory[]>([]);
  const [loading, setLoading] = useState(true);

  // Form State
  const [supplierId, setSupplierId] = useState('');
  const [rows, setRows] = useState<PurchaseItemRow[]>([
    { productId: 0, quantity: 10, costPrice: 0 },
  ]);
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [supRes, prodRes, histRes] = await Promise.all([
        api.get('/suppliers'),
        api.get('/products'),
        api.get('/purchases'),
      ]);
      setSuppliers(supRes.data);
      setProducts(prodRes.data);
      setHistory(histRes.data);
      if (supRes.data.length > 0) setSupplierId(supRes.data[0].id.toString());
      if (prodRes.data.length > 0) {
        setRows([{ productId: prodRes.data[0].id, quantity: 10, costPrice: Math.round(Number(prodRes.data[0].price) * 0.75) }]);
      }
    } catch (err) {
      console.error('Failed to load purchase data', err);
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
        quantity: 10,
        costPrice: firstProd ? Math.round(Number(firstProd.price) * 0.75) : 0,
      },
    ]);
  };

  const removeRow = (index: number) => {
    if (rows.length === 1) return;
    setRows(rows.filter((_, i) => i !== index));
  };

  const updateRow = (index: number, field: keyof PurchaseItemRow, val: any) => {
    const updated = [...rows];
    if (field === 'productId') {
      const selected = products.find((p) => p.id === Number(val));
      updated[index].productId = Number(val);
      if (selected) {
        updated[index].costPrice = Math.round(Number(selected.price) * 0.75);
      }
    } else {
      updated[index][field] = Number(val);
    }
    setRows(updated);
  };

  const calculateTotal = () => {
    return rows.reduce((sum, r) => sum + r.quantity * (r.costPrice || 0), 0);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setSubmitting(true);

    try {
      if (!supplierId) throw new Error('Please select a supplier');
      if (rows.some((r) => !r.productId || r.quantity <= 0)) {
        throw new Error('All rows must have a selected product and quantity > 0');
      }

      await api.post('/purchases', {
        supplierId: Number(supplierId),
        items: rows.map((r) => ({
          productId: Number(r.productId),
          quantity: Number(r.quantity),
          costPrice: Number(r.costPrice),
        })),
      });

      setSuccessMsg('Purchase recorded successfully! Inventory stock increased.');
      loadData();
    } catch (err: any) {
      setErrorMsg(err.response?.data?.message || err.message || 'Failed to record purchase');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl">
      {/* Restocking Entry Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center space-x-3 pb-4 border-b border-slate-100">
          <div className="h-10 w-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
            <ShoppingCart className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">Record New Purchase (Stock Inflow)</h2>
            <p className="text-xs text-slate-500">
              Increase product quantities automatically via verified supplier purchase orders
            </p>
          </div>
        </div>

        {successMsg && (
          <div className="mt-4 p-3 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center space-x-2 text-emerald-700 text-xs font-semibold">
            <CheckCircle2 className="h-4 w-4 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {errorMsg && (
          <div className="mt-4 p-3 rounded-xl bg-rose-50 border border-rose-200 flex items-center space-x-2 text-rose-700 text-xs font-semibold">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-6">
          <div className="max-w-md">
            <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider mb-1.5">
              Select Supplier
            </label>
            <div className="relative">
              <Truck className="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <select
                required
                value={supplierId}
                onChange={(e) => setSupplierId(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm font-medium text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                {suppliers.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Item Rows */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Purchase Items
              </label>
              <button
                type="button"
                onClick={addRow}
                className="flex items-center space-x-1 text-xs font-semibold text-blue-600 hover:text-blue-700"
              >
                <Plus className="h-3.5 w-3.5" />
                <span>Add Item Row</span>
              </button>
            </div>

            <div className="space-y-3">
              {rows.map((row, idx) => {
                const selectedProd = products.find((p) => p.id === row.productId);
                return (
                  <div
                    key={idx}
                    className="flex flex-wrap sm:flex-nowrap items-center gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200"
                  >
                    <div className="flex-1 min-w-[200px]">
                      <span className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                        Product
                      </span>
                      <select
                        required
                        value={row.productId}
                        onChange={(e) => updateRow(idx, 'productId', e.target.value)}
                        className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-800 focus:ring-2 focus:ring-blue-500"
                      >
                        {products.map((p) => (
                          <option key={p.id} value={p.id}>
                            {p.name} ({p.sku}) [Current: {p.quantity}]
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="w-28">
                      <span className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                        Quantity
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

                    <div className="w-36">
                      <span className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                        Cost Price (₹)
                      </span>
                      <input
                        type="number"
                        step="0.01"
                        min="0"
                        required
                        value={row.costPrice}
                        onChange={(e) => updateRow(idx, 'costPrice', e.target.value)}
                        className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm font-mono text-slate-800 focus:ring-2 focus:ring-blue-500"
                      />
                    </div>

                    <div className="w-32 text-right">
                      <span className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                        Subtotal
                      </span>
                      <p className="py-2 text-sm font-bold text-slate-900">
                        ₹{(row.quantity * (row.costPrice || 0)).toLocaleString('en-IN')}
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
          </div>

          {/* Grand Total & Submit */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
            <div>
              <p className="text-xs text-slate-500">Order Total Calculation</p>
              <h3 className="text-2xl font-black text-slate-900">
                ₹{calculateTotal().toLocaleString('en-IN')}
              </h3>
            </div>
            <button
              type="submit"
              disabled={submitting}
              className="w-full sm:w-auto px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm rounded-xl shadow-md shadow-blue-500/20 transition-all disabled:opacity-50"
            >
              {submitting ? 'Updating Inventory...' : 'Submit Purchase & Restock'}
            </button>
          </div>
        </form>
      </div>

      {/* Past Purchases History */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-5 border-b border-slate-100 flex items-center space-x-2">
          <History className="h-5 w-5 text-slate-400" />
          <h3 className="text-base font-bold text-slate-900">Purchase Order History</h3>
        </div>

        {history.length > 0 ? (
          <div className="divide-y divide-slate-100">
            {history.map((pur) => (
              <div key={pur.id} className="p-5 hover:bg-slate-50/50 transition-colors space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <span className="font-mono text-xs font-bold text-blue-600">PO #{pur.id}</span>
                    <span className="text-slate-400 mx-2">•</span>
                    <span className="text-sm font-bold text-slate-800">{pur.supplier?.name}</span>
                    <span className="text-slate-400 mx-2">•</span>
                    <span className="text-xs text-slate-500">
                      {new Date(pur.date).toLocaleDateString('en-IN', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric',
                      })}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-base font-black text-slate-900">
                      ₹{Number(pur.total).toLocaleString('en-IN')}
                    </span>
                    <p className="text-[11px] text-slate-400">By {pur.user?.name}</p>
                  </div>
                </div>

                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 flex flex-wrap gap-3">
                  {pur.items.map((item) => (
                    <div
                      key={item.id}
                      className="text-xs text-slate-700 flex items-center space-x-1.5 bg-white px-2.5 py-1 rounded-lg border border-slate-200"
                    >
                      <Package className="h-3 w-3 text-slate-400" />
                      <span className="font-semibold">{item.product.name}</span>
                      <span className="text-slate-400">×</span>
                      <span className="font-bold text-blue-600">{item.quantity}</span>
                      <span className="text-slate-400">@ ₹{Number(item.costPrice)}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-12 text-center text-slate-400 text-sm">No purchases recorded yet.</div>
        )}
      </div>
    </div>
  );
}

