// src/app/page.tsx
import React from 'react';
import DisplayCsv from './components/DisplayCsv';

const Home: React.FC = () => {
  return (
    <main>
      <h1>Welcome to the CSV Display App</h1>
      <DisplayCsv />
    </main>
  );
};

export default Home;
