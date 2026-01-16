"use client";
import React from "react";
import { Search } from "lucide-react";

interface SearchBarProps {
    onSearch: (query: string) => void;
}

export function SearchBar({ onSearch }: SearchBarProps) {
    return (
        <div className="glass" style={{
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
            padding: "0.75rem 1.25rem",
            borderRadius: "99px",
            width: "100%",
            maxWidth: "500px",
            border: "1px solid rgba(255,255,255,0.1)"
        }}>
            <Search size={18} color="#a1a1aa" />
            <input
                type="text"
                placeholder="Search memories..."
                onChange={(e) => onSearch(e.target.value)}
                style={{
                    background: "transparent",
                    border: "none",
                    outline: "none",
                    color: "#fff",
                    width: "100%",
                    fontSize: "0.95rem"
                }}
            />
        </div>
    );
}
