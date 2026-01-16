"use client";
import React from "react";
import { Trash2, Calendar, Tag } from "lucide-react";
import { Memory } from "@/lib/api";

interface MemoryCardProps {
    memory: Memory;
    onDelete?: (id: string) => void;
}

export function MemoryCard({ memory, onDelete }: MemoryCardProps) {
    // Parsing date safely
    const dateStr = memory.created_at
        ? new Date(memory.created_at).toLocaleDateString()
        : "Just now";

    return (
        <div className="glass-card" style={{ padding: "1.25rem", borderRadius: "12px", display: "flex", flexDirection: "column", gap: "1rem", position: "relative" }}>
            <div style={{ display: "flex", gap: "0.75rem", alignItems: "flex-start" }}>
                <div style={{ width: "40px", height: "40px", borderRadius: "10px", background: "linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1))", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                    <span style={{ fontSize: "1.2rem" }}>💡</span>
                </div>
                <div style={{ flex: 1 }}>
                    <p style={{ fontSize: "1rem", lineHeight: "1.5", color: "#e5e5e5" }}>{memory.memory}</p>
                </div>
            </div>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingTop: "0.75rem", borderTop: "1px solid rgba(255,255,255,0.05)" }}>
                <div style={{ display: "flex", gap: "1rem" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "0.4rem", color: "#737373", fontSize: "0.8rem" }}>
                        <Calendar size={14} />
                        <span>{dateStr}</span>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: "0.4rem", color: "var(--primary)", fontSize: "0.8rem", background: "rgba(139,92,246,0.1)", padding: "2px 8px", borderRadius: "6px" }}>
                        <Tag size={12} />
                        <span>{memory.user_id}</span>
                    </div>
                </div>

                {onDelete && (
                    <button
                        onClick={() => onDelete(memory.id)}
                        style={{ padding: "6px", borderRadius: "6px", border: "none", background: "transparent", color: "#525252", cursor: "pointer", transition: "color 0.2s" }}
                        onMouseEnter={(e) => e.currentTarget.style.color = "#ef4444"}
                        onMouseLeave={(e) => e.currentTarget.style.color = "#525252"}
                    >
                        <Trash2 size={16} />
                    </button>
                )}
            </div>
        </div>
    );
}
