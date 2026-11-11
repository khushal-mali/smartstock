'use client';

import React from 'react';
import { useAuth } from '@/lib/auth-context';
import { Bell, Shield, User } from 'lucide-react';

export default function Navbar({ title }: { title: string }) {
  const { user, isAdmin } = useAuth();

  return (
    <header className="h-16 border-b border-slate-200 bg-white px-6 flex items-center justify-between sticky top-0 z-10">
      <div>
        <h2 className="text-xl font-bold text-slate-800">{title}</h2>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 text-xs font-medium text-slate-600 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200">
          {isAdmin ? (
            <Shield className="h-3.5 w-3.5 text-emerald-600" />
          ) : (
            <User className="h-3.5 w-3.5 text-blue-600" />
          )}
          <span>{user?.name}</span>
          <span className="text-slate-400">|</span>
          <span className={isAdmin ? 'text-emerald-700 font-bold' : 'text-blue-700 font-bold'}>
            {user?.role}
          </span>
        </div>
      </div>
    </header>
  );
}

