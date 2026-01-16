"use client";
import React from 'react';
import { Sidebar } from "@/components/Sidebar";

export function ClientLayout({ children }: { children: React.ReactNode }) {
    return (
        <>
            <Sidebar />
            <main style={{
                padding: "2rem 3rem 2rem 2.5rem",
                paddingLeft: "calc(var(--sidebar-width) + 5rem)",
                marginLeft: "0",
                width: "100%",
                minHeight: "100vh",
                boxSizing: "border-box"
            }}>
                {children}
            </main>
        </>
    );
}
