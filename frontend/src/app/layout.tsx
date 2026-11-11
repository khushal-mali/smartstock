import type { Metadata } from 'next';
import './globals.css';
import { AuthProvider } from '@/lib/auth-context';
import AppLayout from '@/components/AppLayout';

export const metadata: Metadata = {
  title: 'SmartStock – Inventory Management System',
  description: 'Inventory Management System for Small Retail & Warehouses',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <AuthProvider>
          <AppLayout>{children}</AppLayout>
        </AuthProvider>
      </body>
    </html>
  );
}
