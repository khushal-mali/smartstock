'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import {
  LayoutDashboard,
  Package,
  Tags,
  Truck,
  ShoppingCart,
  Receipt,
  BarChart3,
  Users,
  LogOut,
  ShieldCheck,
  UserCheck,
} from 'lucide-react';

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout, isAdmin } = useAuth();

  const navItems = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Products', href: '/products', icon: Package },
    { name: 'Categories', href: '/categories', icon: Tags },
    { name: 'Suppliers', href: '/suppliers', icon: Truck },
    { name: 'Purchases', href: '/purchases', icon: ShoppingCart },
    { name: 'Sales / Billing', href: '/sales', icon: Receipt },
    { name: 'Reports', href: '/reports', icon: BarChart3 },
    ...(isAdmin ? [{ name: 'User Management', href: '/users', icon: Users }] : []),
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-100 flex flex-col h-screen sticky top-0 border-r border-slate-800">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800 flex items-center space-x-3">
        <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <Package className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-lg tracking-tight text-white">SmartStock</h1>
          <p className="text-xs text-slate-400 font-medium">Inventory System</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* User Info & Logout Footer */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/40">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2 overflow-hidden">
            <div className="h-8 w-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
              {isAdmin ? (
                <ShieldCheck className="h-4 w-4 text-emerald-400" />
              ) : (
                <UserCheck className="h-4 w-4 text-blue-400" />
              )}
            </div>
            <div className="truncate">
              <p className="text-xs font-semibold text-white truncate">{user?.name || 'User'}</p>
              <span
                className={`inline-block text-[10px] px-1.5 py-0.2 rounded font-semibold uppercase ${
                  isAdmin ? 'bg-emerald-500/10 text-emerald-400' : 'bg-blue-500/10 text-blue-400'
                }`}
              >
                {user?.role}
              </span>
            </div>
          </div>
        </div>

        <button
          onClick={logout}
          className="w-full flex items-center justify-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 border border-rose-500/20 transition-colors"
        >
          <LogOut className="h-3.5 w-3.5" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}

