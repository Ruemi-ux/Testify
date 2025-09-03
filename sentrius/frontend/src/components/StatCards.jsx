import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

function countBySeverity(findings) {
  const counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0, INFO: 0 };
  findings.forEach((f) => {
    if (counts[f.severity] !== undefined) counts[f.severity]++;
  });
  return counts;
}

function StatCards({ findings }) {
  const counts = countBySeverity(findings);
  const data = Object.keys(counts).map((sev) => ({ name: sev, value: counts[sev] }));

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
      {Object.keys(counts).map((sev) => (
        <div key={sev} className="bg-white rounded-lg shadow p-4">
          <div className="text-sm font-medium text-gray-500">{sev}</div>
          <div className="text-2xl font-bold">{counts[sev]}</div>
        </div>
      ))}
      <div className="col-span-full h-60">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default StatCards;
