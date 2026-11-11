'use client';

import React, { useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { user, token, loading } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const isLoginPage = pathname === '/login';

  useEffect(() => {
    if (!loading && !token && !isLoginPage) {
      router.push('/login');
    }
    if (!loading && token && isLoginPage) {
      router.push('/');
    }
  }, [loading, token, isLoginPage, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-500">Loading SmartStock...</p>
        </div>
      </div>
    );
  }

  if (isLoginPage) {
    return <>{children}</>;
  }

  if (!token) {
    return null;
  }

  // Get Title based on pathname
  const getPageTitle = (path: string) => {
    if (path === '/') return 'Dashboard & Inventory Overview';
    if (path.startsWith('/products')) return 'Product Inventory';
    if (path.startsWith('/categories')) return 'Category Management';
    if (path.startsWith('/suppliers')) return 'Supplier Directory';
    if (path.startsWith('/purchases')) return 'Purchase Orders & Restocking';
    if (path.startsWith('/sales')) return 'Sales & Billing Counter (POS)';
    if (path.startsWith('/reports')) return 'Inventory & Financial Reports';
    if (path.startsWith('/users')) return 'Staff & User Management';
    return 'SmartStock';
  };

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar title={getPageTitle(pathname)} />
        <main className="flex-1 p-6 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}

