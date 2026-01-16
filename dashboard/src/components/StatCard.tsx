import React from "react";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";

interface StatCardProps {
    label: string;
    value: string | number;
    trend?: string;
    trendUp?: boolean;
    icon?: React.ElementType;
}

export function StatCard({ label, value, trend, trendUp, icon: Icon }: StatCardProps) {
    return (
        <div className="glass-card neon-border" style={{ padding: "1.5rem", borderRadius: "16px", flex: 1 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1rem" }}>
                <p style={{ color: "#a1a1aa", fontSize: "0.875rem", fontWeight: 500 }}>{label}</p>
                {Icon && <div style={{ padding: "8px", background: "rgba(255,255,255,0.05)", borderRadius: "8px" }}><Icon size={18} color="#fff" /></div>}
            </div>

            <div style={{ display: "flex", alignItems: "baseline", gap: "0.75rem" }}>
                <h3 style={{ fontSize: "2rem", fontWeight: "700", lineHeight: 1 }}>{value}</h3>
            </div>

            {trend && (
                <div style={{ display: "flex", alignItems: "center", gap: "0.25rem", marginTop: "0.75rem", fontSize: "0.875rem" }}>
                    {trendUp ? <ArrowUpRight size={16} color="#10b981" /> : <ArrowDownRight size={16} color="#ef4444" />}
                    <span style={{ color: trendUp ? "#10b981" : "#ef4444" }}>{trend}</span>
                    <span style={{ color: "#525252", marginLeft: "0.25rem" }}>vs last week</span>
                </div>
            )}
        </div>
    );
}
