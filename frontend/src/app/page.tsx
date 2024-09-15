'use client';

import { useState } from 'react';

import React from 'react';
import Link from 'next/link';
import styled from 'styled-components';
import DisplayCsv from './components/DisplayCsv';

// Styled components
const MainContainer = styled.main`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: #f9f9f9;
  min-height: 100vh;
`;

const Heading = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: #0a2b61;
`;

const Nav = styled.nav`
  margin-bottom: 2rem;
`;

const NavList = styled.ul`
  display: flex;
  gap: 1rem;
  list-style-type: none;
  padding: 0;
`;

const NavItem = styled.li`
  font-size: 1.2rem;
`;

const NavLink = styled(Link)`
  color: #0070f3;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
`;

const Home: React.FC = () => {
  return (
    <MainContainer>
      <Heading>Welcome to the CSV Display App</Heading>

      {/* Navigation Links */}
      <Nav>
        <NavList>
          <NavItem>
            <NavLink href="/">Home</NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="/addData">Add Data</NavLink> {/* Link to the new addData page */}
          </NavItem>
        </NavList>
      </Nav>

      {/* CSV Display Component */}
      <DisplayCsv />
    </MainContainer>
  );
};

export default Home;
