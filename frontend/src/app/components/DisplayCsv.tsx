"use client";

import React, { useState, useEffect } from 'react';

interface CsvRow {
  [key: string]: string | number;
}

const DisplayCsv: React.FC = () => {
  const [csvData, setCsvData] = useState<CsvRow[]>([]);
  const [originalData, setOriginalData] = useState<CsvRow[]>([]);
  const [csvFiles, setCsvFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [sortColumn, setSortColumn] = useState<string>('');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [filtered, setFiltered] = useState<boolean>(false);

  const excludedColumns = ['Number', 'FC', 'GS', 'LOB']; // Columns to exclude

  const fetchCsvFiles = async () => {
    try {
      const response = await fetch('/api/listCsvFiles');
      const result = await response.json();

      if (response.ok) {
        setCsvFiles(result.csvFiles); // Include all files in the dropdown
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to fetch CSV file list');
    }
  };

  const fetchCsvData = async (fileName: string) => {
    try {
      const response = await fetch(`/api/readCsv?team=${fileName.replace('_stats.csv', '')}`);
      const result = await response.json();

      if (response.ok) {
        const data = parseCsvData(result.data);
        setOriginalData(data); // Store original data for undo functionality
        setCsvData(data);
        setError('');
      } else {
        setError(result.error);
        setCsvData([]);
        setOriginalData([]);
      }
    } catch (err) {
      setError('Failed to fetch data');
      setCsvData([]);
      setOriginalData([]);
    }
  };

  const fetchAllCsvData = async () => {
    try {
      let combinedData: CsvRow[] = [];

      // Exclude league_stats.csv when fetching data for "All"
      const filesToFetch = csvFiles.filter(file => file !== 'league_stats.csv');

      for (const file of filesToFetch) {
        const teamName = file.replace('_stats.csv', ''); // Extract team name
        const response = await fetch(`/api/readCsv?team=${teamName}`);
        const result = await response.json();

        if (response.ok) {
          const data = parseCsvData(result.data, true); // Parse and append data
          // Add team column right after the 'Name' column
          const dataWithTeam = data.map(row => {
            const { Name, ...rest } = row;
            return { Name, Team: teamName, ...rest };
          });
          combinedData = combinedData.concat(dataWithTeam);
        }
      }

      setOriginalData(combinedData); // Store original data for undo functionality
      setCsvData(combinedData);
      setError('');
    } catch (err) {
      setError('Failed to fetch data');
      setCsvData([]);
      setOriginalData([]);
    }
  };

  const parseCsvData = (data: string, returnData = false): CsvRow[] => {
    const rows = data.split('\n');
    const headers = rows[0].split(',');

    const parsedData = rows.slice(1).map((row) => {
      const values = row.split(',');

      // Only create a row if it has meaningful content
      if (values.every(value => value.trim() === '')) {
        return null; // Skip empty rows
      }

      const rowData: CsvRow = {};
      headers.forEach((header, index) => {
        rowData[header] = isNaN(Number(values[index])) ? values[index].trim() : Number(values[index]);
      });

      // Skip rows where the 'Number' is 0 and all other stats are blank or 0
      if (rowData['Number'] === 0 && Object.values(rowData).every(value => value === '' || value === 0)) {
        return null;
      }

      return rowData;
    }).filter(row => row !== null); // Filter out any null rows

    if (returnData) {
      return parsedData as CsvRow[];
    }

    return parsedData as CsvRow[];
  };

  // Function to toggle filter based on minimum plate appearance requirement
  const toggleFilterByPlateAppearance = () => {
    if (filtered) {
      // Undo filter by restoring original data
      setCsvData(originalData);
      setFiltered(false);
    } else {
      // Apply filter
      const maxGames = Math.max(...originalData.map(row => (typeof row['Games'] === 'number' ? row['Games'] : 0)));
      const minPlateAppearance = 2.41 * maxGames;

      const filteredData = originalData.filter(row => (typeof row['PA'] === 'number' ? row['PA'] >= minPlateAppearance : false));
      setCsvData(filteredData);
      setFiltered(true);
    }
  };

  useEffect(() => {
    fetchCsvFiles();
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedFile = event.target.value;
    setSelectedFile(selectedFile);

    if (selectedFile === 'all') {
      fetchAllCsvData();
    } else if (selectedFile) {
      fetchCsvData(selectedFile);
    }

    setFiltered(false); // Reset filter status on new file selection
  };

  const handleSort = (column: string) => {
    const newOrder = sortColumn === column && sortOrder === 'asc' ? 'desc' : 'asc';
    setSortColumn(column);
    setSortOrder(newOrder);

    const sortedData = [...csvData].sort((a, b) => {
      if (a[column] < b[column]) return newOrder === 'asc' ? -1 : 1;
      if (a[column] > b[column]) return newOrder === 'asc' ? 1 : -1;
      return 0;
    });

    setCsvData(sortedData);
  };

  // Format numbers to three decimal places
  const formatNumber = (value: any): string => {
    return typeof value === 'number' ? value.toFixed(3) : value;
  };

  return (
    <div>
      <h2>Display CSV Data</h2>
      <label htmlFor="file-select">Choose a file:</label>
      <select id="file-select" value={selectedFile} onChange={handleFileChange} className="select">
        <option value="">--Select a file--</option>
        <option value="all">All</option> {/* Option to display all tables, excluding league_stats.csv */}
        {csvFiles.map((file, index) => (
          <option key={index} value={file}>
            {file.replace('_stats.csv', '')}
          </option>
        ))}
      </select>

      <button onClick={toggleFilterByPlateAppearance} className="button" disabled={csvData.length === 0}>
        {filtered ? 'Undo Filter' : 'Apply Filter by Minimum Plate Appearances'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {csvData.length > 0 && (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                {Object.keys(csvData[0])
                  .filter(header => !excludedColumns.includes(header)) // Exclude specified columns
                  .map((header, index) => (
                    <th
                      key={index}
                      onClick={() => handleSort(header)}
                      className={header === 'Name' ? 'sticky-column' : ''}
                    >
                      {header} {sortColumn === header ? (sortOrder === 'asc' ? '▲' : '▼') : ''}
                    </th>
                  ))}
              </tr>
            </thead>
            <tbody>
              {csvData.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {Object.entries(row)
                    .filter(([key]) => !excludedColumns.includes(key)) // Exclude specified columns
                    .map(([key, value], colIndex) => (
                      <td key={colIndex} className={key === 'Name' ? 'sticky-column' : ''}>
                        {['AVG', 'OBP', 'SLG', 'OPS', 'BABIP', 'ISOP', 'wOBA'].includes(key)
                          ? formatNumber(value)
                          : value}
                      </td>
                    ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default DisplayCsv;
