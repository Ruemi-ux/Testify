import React from 'react';

const severityOptions = ['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'];

function Filters({ filters, setFilters, findings }) {
  const toolOptions = ['ALL', ...Array.from(new Set(findings.map((f) => f.tool)))];

  return (
    <div className="flex flex-wrap gap-4 items-end">
      <div className="flex flex-col">
        <label className="text-sm font-medium mb-1">Severity</label>
        <select
          className="border rounded-md px-2 py-1"
          value={filters.severity}
          onChange={(e) => setFilters({ ...filters, severity: e.target.value })}
        >
          {severityOptions.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
      </div>
      <div className="flex flex-col">
        <label className="text-sm font-medium mb-1">Tool</label>
        <select
          className="border rounded-md px-2 py-1"
          value={filters.tool}
          onChange={(e) => setFilters({ ...filters, tool: e.target.value })}
        >
          {toolOptions.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
      </div>
      <div className="flex flex-col flex-1">
        <label className="text-sm font-medium mb-1">Search</label>
        <input
          type="text"
          className="border rounded-md px-2 py-1 w-full"
          placeholder="Search message or file"
          value={filters.search}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
        />
      </div>
    </div>
  );
}

export default Filters;
