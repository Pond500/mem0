"use client";
import React, { useEffect, useState } from "react";
import useSWR from "swr";
import { api, Memory } from "@/lib/api";
import { StatCard } from "@/components/StatCard";
import { MemoryCard } from "@/components/MemoryCard";
import { Brain, Users, Activity, Loader2 } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
  const { data: memoriesData, error, isLoading } = useSWR('all_memories', () => api.getAll());

  // Debug logging
  console.log("🔍 Dashboard Debug:", { memoriesData, error, isLoading });

  // Safe parsing of memory data which might be array or object
  const memories: Memory[] = Array.isArray(memoriesData)
    ? memoriesData
    : (memoriesData?.results || []);

  console.log("📊 Parsed memories:", memories);

  const totalMemories = memories.length;
  // Mock users for now since API doesn't list them easily without iteration
  const activeUsers = new Set(memories.map(m => m.user_id)).size || 0;

  const recentMemories = [...memories]
    .sort((a, b) => (new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime()))
    .slice(0, 6);

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
      {/* Header */}
      <header style={{ marginBottom: "3rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 className="text-gradient" style={{ fontSize: "2.5rem", fontWeight: "bold", marginBottom: "0.5rem" }}>
            Dashboard
          </h1>
          <p style={{ color: "#a1a1aa" }}>Overview of your AI memory system</p>
        </div>
      </header>

      {/* Stats Row */}
      <div style={{ display: "flex", gap: "1.5rem", marginBottom: "3rem", flexWrap: "wrap" }}>
        <StatCard label="Total Memories" value={totalMemories} trend="+12%" trendUp icon={Brain} />
        <StatCard label="Active Users" value={activeUsers} trend="+5%" trendUp icon={Users} />
        <StatCard label="API Calls" value="89,120" trend="+8%" trendUp icon={Activity} />
      </div>

      {/* Recent Activity Section */}
      <section>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
          <h2 style={{ fontSize: "1.25rem", fontWeight: "600", color: "#fff" }}>Recent Memories</h2>
          <Link href="/memories" style={{ color: "var(--primary)", fontSize: "0.9rem", textDecoration: "none" }}>
            View All &rarr;
          </Link>
        </div>

        {isLoading ? (
          <div style={{ display: "flex", justifyContent: "center", padding: "4rem" }}>
            <Loader2 className="animate-spin" color="#8b5cf6" size={32} />
          </div>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "1.5rem" }}>
            {recentMemories.length > 0 ? (
              recentMemories.map((mem) => (
                <MemoryCard key={mem.id} memory={mem} />
              ))
            ) : (
              <div style={{ gridColumn: "1 / -1", padding: "3rem", textAlign: "center", color: "#666", background: "rgba(255,255,255,0.02)", borderRadius: "12px" }}>
                No memories found. Start chatting with your agent!
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
