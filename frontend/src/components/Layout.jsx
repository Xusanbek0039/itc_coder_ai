import React, { useEffect, useState } from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { Moon, Sun, Monitor, LogOut } from 'lucide-react';
import { Button } from './ui/button';
import { motion, AnimatePresence } from 'framer-motion';

export default function Layout() {
    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'system');
    const navigate = useNavigate();

    useEffect(() => {
        const root = window.document.documentElement;
        root.classList.remove('light', 'dark');

        if (theme === 'system') {
            const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
                ? 'dark'
                : 'light';
            root.classList.add(systemTheme);
        } else {
            root.classList.add(theme);
        }
        localStorage.setItem('theme', theme);
    }, [theme]);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
    }

    return (
        <div className="min-h-screen bg-background text-foreground font-sans transition-colors duration-300">
            <nav className="border-b bg-card/50 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex h-16 justify-between items-center">
                        <Link to="/" className="flex items-center space-x-2">
                            <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-teal-400">
                                ITC CodeAI
                            </span>
                        </Link>

                        <div className="flex items-center space-x-4">
                            {theme === 'dark' ? (
                                <Button variant="ghost" size="icon" onClick={() => setTheme('light')}>
                                    <Sun className="h-5 w-5" />
                                </Button>
                            ) : (
                                <Button variant="ghost" size="icon" onClick={() => setTheme('dark')}>
                                    <Moon className="h-5 w-5" />
                                </Button>
                            )}
                            <Button variant="ghost" size="icon" onClick={handleLogout} title="Logout">
                                <LogOut className="h-5 w-5 text-destructive" />
                            </Button>
                        </div>
                    </div>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <AnimatePresence mode="wait">
                    <Outlet />
                </AnimatePresence>
            </main>
        </div>
    );
}
