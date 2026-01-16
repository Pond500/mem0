"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Brain, Users, Key, Settings, Zap, Moon, Sun } from "lucide-react";

export function Sidebar() {
    const pathname = usePathname();
    const [theme, setTheme] = useState<'dark' | 'light'>('dark');

    useEffect(() => {
        // Load theme from localStorage on mount
        const savedTheme = localStorage.getItem('theme') as 'dark' | 'light';
        if (savedTheme) {
            setTheme(savedTheme);
            document.documentElement.setAttribute('data-theme', savedTheme);
        }
    }, []);

    const toggleTheme = () => {
        const newTheme = theme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
    };

    const links = [
        { href: "/", label: "Dashboard", icon: LayoutDashboard },
        { href: "/memories", label: "Memories", icon: Brain },
        { href: "/users", label: "Users", icon: Users },
        { href: "/api-keys", label: "API Keys", icon: Key },
        { href: "/settings", label: "Settings", icon: Settings },
    ];

    return (
        <aside
            className="glass"
            style={{
                width: "var(--sidebar-width)",
                height: "100vh",
                position: "fixed",
                top: 0,
                left: 0,
                padding: "2rem",
                display: "flex",
                flexDirection: "column",
                gap: "2rem",
                zIndex: 10,
            }}
        >
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                <div style={{ padding: "0.5rem", background: "rgba(139, 92, 246, 0.2)", borderRadius: "8px" }}>
                    <Zap size={24} color="#8b5cf6" />
                </div>
                <h1 className="neon-text" style={{ fontSize: "1.5rem", fontWeight: "bold", letterSpacing: "-0.02em" }}>
                    Mem0
                </h1>
            </div>

            <nav style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                {links.map((link) => {
                    const isActive = pathname === link.href;
                    const Icon = link.icon;
                    return (
                        <Link
                            key={link.href}
                            href={link.href}
                            className={isActive ? "active-link" : ""}
                            style={{
                                display: "flex",
                                alignItems: "center",
                                gap: "1rem",
                                padding: "0.75rem 1rem",
                                borderRadius: "12px",
                                color: isActive ? "#fff" : "var(--foreground)",
                                background: isActive ? "linear-gradient(90deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%)" : "transparent",
                                border: isActive ? "1px solid rgba(139, 92, 246, 0.3)" : "1px solid transparent",
                                transition: "all 0.2s ease",
                                opacity: isActive ? 1 : 0.7
                            }}
                        >
                            <Icon size={20} color={isActive ? "#a78bfa" : "currentColor"} />
                            <span style={{ fontWeight: isActive ? 600 : 400 }}>{link.label}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Theme Toggle */}
            <button
                onClick={toggleTheme}
                style={{
                    marginTop: "auto",
                    display: "flex",
                    alignItems: "center",
                    gap: "0.75rem",
                    padding: "0.75rem 1rem",
                    borderRadius: "12px",
                    background: "rgba(139, 92, 246, 0.1)",
                    border: "1px solid rgba(139, 92, 246, 0.2)",
                    color: "var(--foreground)",
                    cursor: "pointer",
                    transition: "all 0.2s ease",
                    fontSize: "0.95rem",
                    fontWeight: 500
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.background = "rgba(139, 92, 246, 0.2)";
                    e.currentTarget.style.borderColor = "rgba(139, 92, 246, 0.4)";
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.background = "rgba(139, 92, 246, 0.1)";
                    e.currentTarget.style.borderColor = "rgba(139, 92, 246, 0.2)";
                }}
            >
                {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
                {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
            </button>
        </aside>
    );
}
