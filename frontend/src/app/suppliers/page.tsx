'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useAuth } from '@/lib/auth-context';
import { Truck, Phone, Mail, Plus, Edit2, Trash2, X, Package } from 'lucide-react';

interface Supplier {
  id: number;
  name: string;
  phone: string;
  email: string;
  _count?: { products: number; purchases: number };
}

export default function SuppliersPage() {
  const { isAdmin } = useAuth();
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState<Supplier | null>(null);
  const [formData, setFormData] = useState({ name: '', phone: '', email: '' });
  const [error, setError] = useState('');

  const fetchSuppliers = async () => {
    try {
      setLoading(true);
      const res = await api.get('/suppliers');
      setSuppliers(res.data);
    } catch (err) {
      console.error('Failed to load suppliers', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSuppliers();
  }, []);

  const openAdd = () => {
    setEditingSupplier(null);
    setFormData({ name: '', phone: '', email: '' });
    setError('');
    setIsModalOpen(true);
  };

  const openEdit = (sup: Supplier) => {
    setEditingSupplier(sup);
    setFormData({ name: sup.name, phone: sup.phone, email: sup.email });
    setError('');
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      if (editingSupplier) {
        await api.put(`/suppliers/${editingSupplier.id}`, formData);
      } else {
        await api.post('/suppliers', formData);
      }
      setIsModalOpen(false);
      fetchSuppliers();
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to save supplier');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this supplier?')) return;
    try {
      await api.delete(`/suppliers/${id}`);
      fetchSuppliers();
    } catch (err: any) {
      alert(err.response?.data?.message || 'Failed to delete supplier');
    }
  };

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Supplier Directory</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Manage vendor profiles, purchase links, and contact channels
          </p>
        </div>
        {isAdmin && (
          <button
            onClick={openAdd}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold shadow-sm transition-all"
          >
            <Plus className="h-4 w-4" />
            <span>Add Supplier</span>
          </button>
        )}
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center">
            <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          </div>
        ) : suppliers.length > 0 ? (
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="py-3 px-4">Supplier Name</th>
                <th className="py-3 px-4">Phone Number</th>
                <th className="py-3 px-4">Email</th>
                <th className="py-3 px-4">Supplied Products</th>
                {isAdmin && <th className="py-3 px-4 text-right">Actions</th>}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {suppliers.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3 px-4 font-semibold text-slate-900 flex items-center space-x-2">
                    <Truck className="h-4 w-4 text-indigo-500 shrink-0" />
                    <span>{s.name}</span>
                  </td>
                  <td className="py-3 px-4 text-slate-600">
                    <div className="flex items-center space-x-1.5">
                      <Phone className="h-3.5 w-3.5 text-slate-400" />
                      <span>{s.phone}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-slate-600">
                    <div className="flex items-center space-x-1.5">
                      <Mail className="h-3.5 w-3.5 text-slate-400" />
                      <span>{s.email}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
                      <Package className="h-3 w-3 text-slate-400" />
                      <span>{s._count?.products || 0} products</span>
                    </span>
                  </td>
                  {isAdmin && (
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end space-x-2">
                        <button
                          onClick={() => openEdit(s)}
                          className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="Edit"
                        >
                          <Edit2 className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(s.id)}
                          className="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="p-12 text-center text-slate-400 text-sm">No suppliers registered.</div>
        )}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-base text-slate-900">
                {editingSupplier ? 'Edit Supplier' : 'New Supplier'}
              </h3>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="h-5 w-5" />
              </button>
            </div>

            {error && (
              <div className="mt-3 p-2.5 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Company / Supplier Name</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g. Apex Distribution Corp"
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Phone Number</label>
                <input
                  type="text"
                  required
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder="+91 98765 43210"
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Email Address</label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="orders@supplier.com"
                  className="w-full px-3 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </div>

              <div className="pt-2 flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 border border-slate-200 text-slate-600 hover:bg-slate-50 rounded-xl text-xs font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold shadow-sm"
                >
                  Save Supplier
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

