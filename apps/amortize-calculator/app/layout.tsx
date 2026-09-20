import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Loan Amortization Calculator',
  description:
    'Calculate precise loan amortization schedules with decimal-perfect financial math',
  openGraph: {
    title: 'Loan Amortization Calculator',
    description: 'Calculate your loan payments with precision',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
