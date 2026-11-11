'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth-context';
import { Package, Lock, Mail, AlertCircle, ArrowRight } from 'lucide-react';

export default function LoginPage() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed. Please check credentials.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDemoFill = (role: 'ADMIN' | 'STAFF') => {
    if (role === 'ADMIN') {
      setEmail('admin@smartstock.com');
      setPassword('admin123');
    } else {
      setEmail('staff@smartstock.com');
      setPassword('staff123');
    }
    setError('');
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo and title */}
        <div className="text-center mb-8">
          <div className="inline-flex h-14 w-14 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-500 items-center justify-center shadow-xl shadow-blue-500/20 mb-4">
            <Package className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">SmartStock Portal</h1>
          <p className="text-sm text-slate-400 mt-1">
            Inventory Management System
          </p>
        </div>

        {/* Card */}
        <div className="bg-slate-800/80 backdrop-blur-xl border border-slate-700/60 rounded-2xl p-7 shadow-2xl">
          {error && (
            <div className="mb-5 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center space-x-2 text-rose-400 text-xs font-medium">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <Mail className="h-4 w-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@smartstock.com"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900/60 border border-slate-700 rounded-xl text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="h-4 w-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900/60 border border-slate-700 rounded-xl text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full mt-2 py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium text-sm rounded-xl flex items-center justify-center space-x-2 shadow-lg shadow-blue-600/30 transition-all disabled:opacity-50"
            >
              <span>{submitting ? 'Authenticating...' : 'Sign In'}</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>

          {/* Quick Demo Fill Buttons for Reviewers/Examiners */}
          <div className="mt-6 pt-5 border-t border-slate-700/60">
            <p className="text-[11px] font-semibold text-slate-400 text-center uppercase tracking-wider mb-2.5">
              Quick Fill Demo Credentials
            </p>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => handleDemoFill('ADMIN')}
                className="py-1.5 px-3 bg-slate-700/50 hover:bg-slate-700 border border-slate-600/60 rounded-lg text-xs font-medium text-emerald-400 text-center transition-colors"
              >
                Fill Admin (Admin)
              </button>
              <button
                type="button"
                onClick={() => handleDemoFill('STAFF')}
                className="py-1.5 px-3 bg-slate-700/50 hover:bg-slate-700 border border-slate-600/60 rounded-lg text-xs font-medium text-blue-400 text-center transition-colors"
              >
                Fill Staff (Staff)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

