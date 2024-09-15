'use client';

import { useState } from 'react';
import styled from 'styled-components';
import Link from 'next/link';  // Import Link from Next.js

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background-color: #f9f9f9;
  padding: 0;
`;

const Header = styled.header`
  width: 100%;
  background-color: #0a2b61;
  padding: 2rem 0;
  text-align: center;
  color: white;
`;

const HeaderText = styled.h1`
  font-size: 2.5rem;
  margin: 0;
`;

const FormContainer = styled.div`
  width: 100%;
  max-width: 600px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin: 2rem 0;
  padding: 2rem;
  text-align: center;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  align-items: stretch;
`;

const Label = styled.label`
  font-size: 18px;
  margin-bottom: 8px;
  text-align: left;
`;

const TextArea = styled.textarea`
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
  width: 100%;
  height: 200px;
  color: black;
`;

const Button = styled.button`
  padding: 12px;
  font-size: 18px;
  background-color: #0070f3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  align-self: center;
  width: 150px;
`;

const Error = styled.p`
  color: red;
  text-align: center;
`;

const Success = styled.p`
  color: green;
  text-align: center;
`;

const HomeLink = styled.a`
  color: #0070f3;
  font-size: 18px;
  margin-top: 20px;
  cursor: pointer;
  text-decoration: underline;
`;

export default function AddData() {
  const [data, setData] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!data) {
      setError('Please fill in the box with valid data.');
      return;
    }

    try {
      const response = await fetch('/api/addData', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data }),
      });

      if (response.ok) {
        const responseData = await response.json();
        setSuccess(responseData.message);
        setData('');
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to add data');
      }
    } catch (err) {
      setError('Error while adding data');
    }
  };

  return (
    <PageContainer>
      <Header>
        <HeaderText>Add Data</HeaderText>
      </Header>

      <FormContainer>
        {error && <Error>{error}</Error>}
        {success && <Success>{success}</Success>}

        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label>Enter Data:</Label>
            <TextArea
              value={data}
              onChange={(e) => setData(e.target.value)}
              placeholder="Enter your data here..."
              required
            />
          </FormGroup>
          <Button type="submit">Submit</Button>
        </Form>

        {/* Back to Home Link */}
        <Link href="/" passHref>
          <HomeLink>Back to Home</HomeLink>
        </Link>

      </FormContainer>
    </PageContainer>
  );
}
