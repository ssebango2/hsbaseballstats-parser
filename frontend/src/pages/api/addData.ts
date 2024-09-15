import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { name, team, pa, avg } = req.body;

    // Perform basic validation
    if (!name || !team || pa <= 0 || avg <= 0 || avg > 1) {
      return res.status(400).json({ error: 'Invalid input data. Please provide valid player information.' });
    }

    try {
      // Make a POST request to the Python Flask API
      const pythonResponse = await fetch('http://localhost:5000/api/parse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, team, pa, avg }),  // Send the data to the Python API
      });

      if (pythonResponse.ok) {
        const data = await pythonResponse.json();
        return res.status(200).json({ message: 'Player data processed successfully!', data });
      } else {
        return res.status(500).json({ error: 'Failed to process data in the Python backend.' });
      }
    } catch (error) {
      console.error('Error connecting to Python API:', error);
      return res.status(500).json({ error: 'Server error. Please try again later.' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
