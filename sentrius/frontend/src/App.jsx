import React, { useState, useEffect } from 'react';
import { Play, Trash2, Upload as UploadIcon, FileDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import FindingsTable from './components/FindingsTable';
import StatCards from './components/StatCards';
import Filters from './components/Filters';

const API_BASE = import.meta.env.VITE_API_BASE || '/api';
const USE_MOCK = true;

const mockFindings = [
  {
    id: '1',
    tool: 'Trivy',
    severity: 'HIGH',
    message: 'Vulnerability CVE-2023-1234 in dependency abc',
    file: 'package.json',
    line: 0,
  },
  {
    id: '2',
    tool: 'Semgrep',
    severity: 'MEDIUM',
    message: 'SQL injection risk',
    file: 'src/db.js',
    line: 42,
  },
];

const fetchFindings = async (repoUrl) => {
  try {
    const res = await axios.post(`${API_BASE}/scan`, { repo_url: repoUrl });
    return res.data.findings;
  } catch (err) {
    console.error(err);
    return [];
  }
};

function App() {
  const [repoUrl, setRepoUrl] = useState('');
  const [findings, setFindings] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [filters, setFilters] = useState({ severity: 'ALL', tool: 'ALL', search: '' });

  useEffect(() => {
    applyFilters();
  }, [findings, filters]);

  const handleScan = async () => {
    let results = [];
    if (USE_MOCK) {
      results = mockFindings;
    } else {
      results = await fetchFindings(repoUrl);
    }
    setFindings(results);
  };

  const handleClear = () => {
    setFindings([]);
    setRepoUrl('');
  };

  const applyFilters = () => {
    let data = [...findings];
    if (filters.severity !== 'ALL') {
      data = data.filter((f) => f.severity === filters.severity);
    }
    if (filters.tool !== 'ALL') {
      data = data.filter((f) => f.tool === filters.tool);
    }
    if (filters.search) {
      const term = filters.search.toLowerCase();
      data = data.filter((f) =>
        f.message.toLowerCase().includes(term) || f.file.toLowerCase().includes(term)
      );
    }
    setFiltered(data);
  };

  const handleExportCSV = () => {
    const csv = [
      ['Tool', 'Severity', 'Message', 'File', 'Line'],
      ...findings.map((f) => [f.tool, f.severity, f.message, f.file, f.line]),
    ]
      .map((row) => row.map((item) => `"${item}"`).join(','))
      .join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'findings.csv';
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleExportSplunk = async () => {
    try {
      await axios.post(`${API_BASE}/export_splunk`, { findings });
      alert('Export an Splunk gesendet.');
    } catch (err) {
      console.error(err);
      alert('Export fehlgeschlagen.');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-indigo-600 text-white px-6 py-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Sentrius</h1>
        <div className="flex gap-2">
          <input
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            className="px-3 py-1 rounded-md text-gray-900"
            placeholder="Repository URL"
          />
          <button
            onClick={handleScan}
            className="flex items-center gap-1 bg-white text-indigo-600 px-3 py-1 rounded-md hover:bg-indigo-100"
          >
            <Play size={16} /> Scan
          </button>
          <button
            onClick={handleClear}
            className="flex items-center gap-1 bg-white text-indigo-600 px-3 py-1 rounded-md hover:bg-indigo-100"
          >
            <Trash2 size={16} /> Clear
          </button>
        </div>
      </header>

      <main className="flex-1 p-6 space-y-6">
        <Filters filters={filters} setFilters={setFilters} findings={findings} />
        <StatCards findings={filtered} />
        <div className="flex justify-end gap-2">
          <button
            onClick={handleExportCSV}
            className="flex items-center gap-1 bg-indigo-600 text-white px-3 py-1 rounded-md hover:bg-indigo-700"
          >
            <FileDown size={16} /> CSV Export
          </button>
          <button
            onClick={handleExportSplunk}
            className="flex items-center gap-1 bg-indigo-600 text-white px-3 py-1 rounded-md hover:bg-indigo-700"
          >
            <UploadIcon size={16} /> Splunk Export
          </button>
        </div>
        <AnimatePresence>
          <FindingsTable findings={filtered} />
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
