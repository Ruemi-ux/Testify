import React from 'react';
import { motion } from 'framer-motion';

const rowVariants = {
  hidden: { opacity: 0, y: -10 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.05 },
  }),
};

function FindingsTable({ findings }) {
  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Tool</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Severity</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Message</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">File</th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Line</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {findings.map((f, idx) => (
            <motion.tr
              key={f.id || idx}
              custom={idx}
              initial="hidden"
              animate="visible"
              variants={rowVariants}
            >
              <td className="px-4 py-2 whitespace-nowrap">{f.tool}</td>
              <td className="px-4 py-2 whitespace-nowrap">{f.severity}</td>
              <td className="px-4 py-2">{f.message}</td>
              <td className="px-4 py-2 whitespace-nowrap">{f.file}</td>
              <td className="px-4 py-2 whitespace-nowrap">{f.line}</td>
            </motion.tr>
          ))}
        </tbody>
      </table>
      {findings.length === 0 && (
        <div className="p-4 text-center text-gray-500">Keine Findings gefunden.</div>
      )}
    </div>
  );
}

export default FindingsTable;
