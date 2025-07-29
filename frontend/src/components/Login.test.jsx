import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Login from './Login';

describe('Login Component', () => {
  it('renders the login form', () => {
    render(
      <Router>
        <Login />
      </Router>
    );
    expect(screen.getByPlaceholderText(/tu@email.com/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/••••••••/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Iniciar Sesión/i })).toBeInTheDocument();
  });
});

