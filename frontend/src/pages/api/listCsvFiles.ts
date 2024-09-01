// src/pages/api/listCsvFiles.ts
import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const outputDir = '/Users/bkkim/baseball-stats-app/output_data'; // Use the actual absolute path

  try {
    const files = fs.readdirSync(outputDir);
    const csvFiles = files.filter(file => file.endsWith('.csv'));
    res.status(200).json({ csvFiles });
  } catch (error) {
    console.error('Error reading directory:', error);
    res.status(500).json({ error: 'Failed to read directory' });
  }
}
