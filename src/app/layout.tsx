// src/app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: '西雅图亲子活动 | Seattle Kids Weekend',
  description: '大西雅图地区周末家庭与儿童活动聚合指南',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN" className={`${inter.variable} antialiased selection:bg-slate-200 selection:text-slate-900`}>
      <body className="font-sans text-slate-800 bg-[#f8f9fa] min-h-screen">
        {children}
      </body>
    </html>
  );
}