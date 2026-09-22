import { useState } from 'react';
import { AmortizationScheduleEntry } from '@/lib/calculator';

interface ScheduleTableProps {
  schedule: AmortizationScheduleEntry[];
}

export default function ScheduleTable({ schedule }: ScheduleTableProps) {
  const [showAll, setShowAll] = useState(false);
  const displaySchedule = showAll ? schedule : schedule.slice(0, 12);
  const hasMore = schedule.length > 12;

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="px-8 py-6 bg-gray-900 text-white flex justify-between items-start">
        <div>
          <h2 className="text-2xl font-bold">Amortization Schedule</h2>
          <p className="text-gray-400 text-sm mt-1">
            {showAll ? 'All payments' : 'First 12 months'} {hasMore && `(showing ${displaySchedule.length} of ${schedule.length} total)`}
          </p>
        </div>
        {hasMore && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded transition-colors"
          >
            {showAll ? 'Show First 12' : 'Show All'}
          </button>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100 border-b border-gray-200">
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Month</th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900">Payment</th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900">Principal</th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900">Interest</th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900">Balance</th>
            </tr>
          </thead>
          <tbody>
            {displaySchedule.map((entry, idx) => (
              <tr
                key={entry.month}
                className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
              >
                <td className="px-6 py-4 text-sm text-gray-900 font-medium">
                  {entry.month}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900 text-right font-mono">
                  ${parseFloat(entry.payment).toFixed(2)}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900 text-right font-mono">
                  ${parseFloat(entry.principal).toFixed(2)}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900 text-right font-mono">
                  ${parseFloat(entry.interest).toFixed(2)}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900 text-right font-mono font-semibold">
                  ${parseFloat(entry.balance).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}
