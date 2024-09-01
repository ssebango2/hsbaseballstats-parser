// src/pages/api/readCsv.ts
import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { team } = req.query;

  if (typeof team !== 'string') {
    return res.status(400).json({ error: 'Invalid team name' });
  }

  // Define the absolute path to the `output_data` directory
  const outputDir = '/Users/bkkim/baseball-stats-app/output_data';
  const filePath = path.join(outputDir, `${team}_stats.csv`);

  // More detailed logging
  console.log('Current working directory:', process.cwd());
  console.log('Looking for file:', filePath);

  // Check if the file exists
  if (!fs.existsSync(filePath)) {
    console.error('File not found at path:', filePath);
    return res.status(404).json({ error: `File not found at path: ${filePath}` });
  }

  // Read the CSV file
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Failed to read file:', filePath, err);
      return res.status(500).json({ error: 'Failed to read the file' });
    }
    res.status(200).json({ data });
  });
}
