'use client';

import { useState, useMemo } from 'react';
import Decimal from 'decimal.js';
import { calculateAmortization } from '@/lib/calculator';
import ScheduleTable from '@/components/ScheduleTable';

export default function AmortizeCalculator() {
  const [principal, setPrincipal] = useState('300000');
  const [rate, setRate] = useState('6');
  const [months, setMonths] = useState('360');

  const { result, error } = useMemo(() => {
    try {
      const p = new Decimal(principal || 0);
      const r = new Decimal(rate || 0);
      const mInput = months || '0';
      const m = parseInt(mInput, 10);

      if (!principal || !rate || !months) return { result: null, error: '' };

      // Validate that months is an integer (not truncated from decimal)
      if (mInput.includes('.') || mInput.includes('e') || mInput.includes('E')) {
        return {
          result: null,
          error: 'Loan term must be a whole number of months',
        };
      }

      return { result: calculateAmortization(p, r, m), error: '' };
    } catch (err) {
      return {
        result: null,
        error: err instanceof Error ? err.message : 'Invalid input',
      };
    }
  }, [principal, rate, months]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Loan Amortization Calculator
          </h1>
          <p className="text-gray-600">
            Calculate precise monthly payments and view your full amortization schedule
          </p>
        </div>

        {/* Calculator Card */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            {/* Principal Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Loan Amount
              </label>
              <div className="relative">
                <span className="absolute left-3 top-3 text-gray-500">$</span>
                <input
                  type="number"
                  value={principal}
                  onChange={(e) => setPrincipal(e.target.value)}
                  className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="0.00"
                  step="100"
                />
              </div>
            </div>

            {/* Rate Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Annual Rate (%)
              </label>
              <div className="relative">
                <input
                  type="number"
                  value={rate}
                  onChange={(e) => setRate(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  max="50"
                />
                <span className="absolute right-3 top-3 text-gray-500">%</span>
              </div>
            </div>

            {/* Term Input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Loan Term (Months)
              </label>
              <input
                type="number"
                value={months}
                onChange={(e) => setMonths(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0"
                step="1"
                min="1"
                max="480"
              />
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {/* Results Summary */}
          {result && (
            <div className="grid md:grid-cols-2 gap-6 p-6 bg-blue-50 rounded-lg">
              <div>
                <p className="text-gray-600 text-sm mb-1">Monthly Payment</p>
                <p className="text-3xl font-bold text-blue-600">
                  ${parseFloat(result.monthly_payment).toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </p>
              </div>
              <div>
                <p className="text-gray-600 text-sm mb-1">Total Interest</p>
                <p className="text-3xl font-bold text-blue-600">
                  ${parseFloat(result.total_interest).toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Schedule Table */}
        {result && <ScheduleTable schedule={result.schedule} />}

        {/* Info Footer */}
        <div className="text-center text-gray-600 text-sm mt-8">
          <p>
            Built with precision financial math • Powered by{' '}
            <a
              href="https://github.com/mir-quadri/amortize-platform"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              Amortize Platform
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
