"use client";
import React, { useState, useMemo } from "react";
import useSWR, { mutate } from "swr";
import { api, Memory } from "@/lib/api";
import { Plus, Loader2, Search, Trash2, ChevronUp, ChevronDown, Tag } from "lucide-react";

type SortField = 'created_at' | 'user_id' | 'memory';
type SortOrder = 'asc' | 'desc';

export default function MemoriesPage() {
    const { data: memoriesData, error, isLoading } = useSWR('all_memories', () => api.getAll());
    const [searchQuery, setSearchQuery] = useState("");
    const [userFilter, setUserFilter] = useState<string>("");
    const [tagFilter, setTagFilter] = useState<string>("");
    const [sortField, setSortField] = useState<SortField>('created_at');
    const [sortOrder, setSortOrder] = useState<SortOrder>('desc');
    const [isAdding, setIsAdding] = useState(false);

    const memories: Memory[] = Array.isArray(memoriesData)
        ? memoriesData
        : (memoriesData?.results || []);

    // Get unique users for filter
    const uniqueUsers = useMemo(() =>
        Array.from(new Set(memories.map(m => m.user_id))).sort(),
        [memories]
    );

    // Get all unique tags for filter
    const allTags = useMemo(() => {
        const tagSet = new Set<string>();
        memories.forEach(m => {
            const tags = m.metadata?.tags || [];
            tags.forEach(tag => tagSet.add(tag));
        });
        return Array.from(tagSet).sort();
    }, [memories]);

    // Filter and sort memories
    const filteredMemories = useMemo(() => {
        let filtered = memories.filter(m => {
            const matchesSearch = m.memory.toLowerCase().includes(searchQuery.toLowerCase()) ||
                m.user_id.toLowerCase().includes(searchQuery.toLowerCase());
            const matchesUser = !userFilter || m.user_id === userFilter;
            const matchesTag = !tagFilter || (m.metadata?.tags || []).includes(tagFilter);
            return matchesSearch && matchesUser && matchesTag;
        });

        // Sort
        filtered.sort((a, b) => {
            let aVal, bVal;
            if (sortField === 'created_at') {
                aVal = new Date(a.created_at || 0).getTime();
                bVal = new Date(b.created_at || 0).getTime();
            } else if (sortField === 'user_id') {
                aVal = a.user_id.toLowerCase();
                bVal = b.user_id.toLowerCase();
            } else {
                aVal = a.memory.toLowerCase();
                bVal = b.memory.toLowerCase();
            }

            if (aVal < bVal) return sortOrder === 'asc' ? -1 : 1;
            if (aVal > bVal) return sortOrder === 'asc' ? 1 : -1;
            return 0;
        });

        return filtered;
    }, [memories, searchQuery, userFilter, tagFilter, sortField, sortOrder]);

    const handleSort = (field: SortField) => {
        if (sortField === field) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            setSortField(field);
            setSortOrder('desc');
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm("Are you sure you want to delete this memory?")) return;
        try {
            await api.delete(id);
            mutate('all_memories');
        } catch (e) {
            alert("Failed to delete memory");
        }
    };

    const handleAdd = async () => {
        const text = prompt("Enter memory text:");
        if (!text) return;
        const userId = prompt("Enter user ID:", "user_default");
        if (!userId) return;

        try {
            setIsAdding(true);
            await api.add(text, userId);
            mutate('all_memories');
        } catch (e) {
            alert("Failed to add memory");
        } finally {
            setIsAdding(false);
        }
    };

    const formatTime = (dateStr?: string) => {
        if (!dateStr) return '-';
        const date = new Date(dateStr);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        const diffDays = Math.floor(diffHours / 24);
        return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    };

    const getTagColor = (tag: string) => {
        const colorMap: Record<string, string> = {
            'work': '#3b82f6',
            'food': '#f59e0b',
            'tech': '#8b5cf6',
            'personal': '#ec4899',
            'travel': '#10b981',
            'health': '#ef4444',
            'sports': '#14b8a6',
            'preference': '#a855f7',
            'career': '#6366f1',
        };
        return colorMap[tag.toLowerCase()] || '#6b7280';
    };

    const SortIcon = ({ field }: { field: SortField }) => {
        if (sortField !== field) return <ChevronUp size={14} style={{ opacity: 0.3 }} />;
        return sortOrder === 'asc'
            ? <ChevronUp size={14} color="#8b5cf6" />
            : <ChevronDown size={14} color="#8b5cf6" />;
    };

    return (
        <div style={{ maxWidth: "1400px", margin: "0 auto" }}>
            {/* Header */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
                <h1 style={{ fontSize: "2rem", fontWeight: "bold" }}>Memories</h1>
                <button
                    onClick={handleAdd}
                    disabled={isAdding}
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                        background: "var(--primary)",
                        color: "white",
                        border: "none",
                        padding: "0.75rem 1.5rem",
                        borderRadius: "8px",
                        cursor: "pointer",
                        fontWeight: 600
                    }}
                >
                    {isAdding ? <Loader2 className="animate-spin" size={20} /> : <Plus size={20} />}
                    Add Memory
                </button>
            </div>

            {/* Filters */}
            <div className="glass-card" style={{ padding: "1.5rem", borderRadius: "12px", marginBottom: "1.5rem" }}>
                <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", alignItems: "center" }}>
                    <div style={{ flex: "1", minWidth: "250px", display: "flex", alignItems: "center", gap: "0.5rem", background: "rgba(0,0,0,0.3)", padding: "0.5rem 1rem", borderRadius: "8px" }}>
                        <Search size={18} color="#a1a1aa" />
                        <input
                            type="text"
                            placeholder="Search memories or users..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
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

                    <select
                        value={userFilter}
                        onChange={(e) => setUserFilter(e.target.value)}
                        style={{
                            background: "rgba(0,0,0,0.3)",
                            border: "1px solid rgba(255,255,255,0.1)",
                            padding: "0.5rem 1rem",
                            borderRadius: "8px",
                            color: "#fff",
                            fontSize: "0.95rem",
                            cursor: "pointer"
                        }}
                    >
                        <option value="">All Users ({uniqueUsers.length})</option>
                        {uniqueUsers.map(user => (
                            <option key={user} value={user}>{user}</option>
                        ))}
                    </select>

                    <select
                        value={tagFilter}
                        onChange={(e) => setTagFilter(e.target.value)}
                        style={{
                            background: "rgba(0,0,0,0.3)",
                            border: "1px solid rgba(255,255,255,0.1)",
                            padding: "0.5rem 1rem",
                            borderRadius: "8px",
                            color: "#fff",
                            fontSize: "0.95rem",
                            cursor: "pointer"
                        }}
                    >
                        <option value="">All Tags ({allTags.length})</option>
                        {allTags.map(tag => (
                            <option key={tag} value={tag}>#{tag}</option>
                        ))}
                    </select>

                    {(searchQuery || userFilter || tagFilter) && (
                        <button
                            onClick={() => { setSearchQuery(""); setUserFilter(""); setTagFilter(""); }}
                            style={{
                                background: "transparent",
                                border: "1px solid rgba(255,255,255,0.2)",
                                padding: "0.5rem 1rem",
                                borderRadius: "8px",
                                color: "#a1a1aa",
                                fontSize: "0.9rem",
                                cursor: "pointer"
                            }}
                        >
                            Reset Filters
                        </button>
                    )}
                </div>
            </div>

            {isLoading ? (
                <div style={{ display: "flex", justifyContent: "center", padding: "4rem" }}>
                    <Loader2 className="animate-spin" color="#8b5cf6" size={32} />
                </div>
            ) : (
                <div className="glass-card" style={{ borderRadius: "12px", overflow: "hidden" }}>
                    <div style={{ overflowX: "auto" }}>
                        <table style={{ width: "100%", borderCollapse: "collapse" }}>
                            <thead>
                                <tr style={{ background: "rgba(255,255,255,0.03)", borderBottom: "1px solid rgba(255,255,255,0.08)" }}>
                                    <th
                                        onClick={() => handleSort('created_at')}
                                        style={{ padding: "1rem", textAlign: "left", fontSize: "0.85rem", color: "#a1a1aa", fontWeight: 600, cursor: "pointer", userSelect: "none" }}
                                    >
                                        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                                            Time <SortIcon field="created_at" />
                                        </div>
                                    </th>
                                    <th
                                        onClick={() => handleSort('memory')}
                                        style={{ padding: "1rem", textAlign: "left", fontSize: "0.85rem", color: "#a1a1aa", fontWeight: 600, cursor: "pointer", userSelect: "none" }}
                                    >
                                        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                                            Memory <SortIcon field="memory" />
                                        </div>
                                    </th>
                                    <th style={{ padding: "1rem", textAlign: "left", fontSize: "0.85rem", color: "#a1a1aa", fontWeight: 600 }}>
                                        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                                            <Tag size={14} /> Tags
                                        </div>
                                    </th>
                                    <th
                                        onClick={() => handleSort('user_id')}
                                        style={{ padding: "1rem", textAlign: "left", fontSize: "0.85rem", color: "#a1a1aa", fontWeight: 600, cursor: "pointer", userSelect: "none" }}
                                    >
                                        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                                            User ID <SortIcon field="user_id" />
                                        </div>
                                    </th>
                                    <th style={{ padding: "1rem", textAlign: "left", fontSize: "0.85rem", color: "#a1a1aa", fontWeight: 600 }}>
                                        Created At
                                    </th>
                                    <th style={{ padding: "1rem", textAlign: "right", fontSize: "0.85rem", color: "#a1a1aa", fontWeight: 600 }}>
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredMemories.length > 0 ? (
                                    filteredMemories.map((mem) => (
                                        <tr
                                            key={mem.id}
                                            style={{ borderBottom: "1px solid rgba(255,255,255,0.05)", transition: "background 0.2s" }}
                                            onMouseEnter={(e) => e.currentTarget.style.background = "rgba(255,255,255,0.02)"}
                                            onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
                                        >
                                            <td style={{ padding: "1rem", fontSize: "0.9rem", color: "#d4d4d8", whiteSpace: "nowrap" }}>
                                                {formatTime(mem.created_at)}
                                            </td>
                                            <td style={{ padding: "1rem", fontSize: "0.9rem", color: "#e5e5e5", maxWidth: "400px" }}>
                                                {mem.memory}
                                            </td>
                                            <td style={{ padding: "1rem" }}>
                                                <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
                                                    {(mem.metadata?.tags || []).map((tag, idx) => (
                                                        <span
                                                            key={idx}
                                                            style={{
                                                                fontSize: "0.75rem",
                                                                color: "#fff",
                                                                background: getTagColor(tag),
                                                                padding: "2px 8px",
                                                                borderRadius: "4px",
                                                                fontWeight: 500,
                                                                opacity: 0.9
                                                            }}
                                                        >
                                                            #{tag}
                                                        </span>
                                                    ))}
                                                    {(!mem.metadata?.tags || mem.metadata.tags.length === 0) && (
                                                        <span style={{ fontSize: "0.75rem", color: "#666" }}>-</span>
                                                    )}
                                                </div>
                                            </td>
                                            <td style={{ padding: "1rem" }}>
                                                <span style={{
                                                    fontSize: "0.85rem",
                                                    color: "var(--primary)",
                                                    background: "rgba(139,92,246,0.1)",
                                                    padding: "4px 10px",
                                                    borderRadius: "6px",
                                                    fontWeight: 500
                                                }}>
                                                    {mem.user_id}
                                                </span>
                                            </td>
                                            <td style={{ padding: "1rem", fontSize: "0.85rem", color: "#a1a1aa" }}>
                                                {mem.created_at ? new Date(mem.created_at).toLocaleDateString() : '-'}
                                            </td>
                                            <td style={{ padding: "1rem", textAlign: "right" }}>
                                                <button
                                                    onClick={() => handleDelete(mem.id)}
                                                    style={{
                                                        padding: "6px 12px",
                                                        borderRadius: "6px",
                                                        border: "1px solid rgba(239,68,68,0.3)",
                                                        background: "rgba(239,68,68,0.1)",
                                                        color: "#ef4444",
                                                        cursor: "pointer",
                                                        fontSize: "0.85rem",
                                                        display: "inline-flex",
                                                        alignItems: "center",
                                                        gap: "0.5rem"
                                                    }}
                                                >
                                                    <Trash2 size={14} /> Delete
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={6} style={{ padding: "3rem", textAlign: "center", color: "#666" }}>
                                            No memories found matching your filters.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>

                    {/* Footer with count */}
                    <div style={{ padding: "1rem 1.5rem", background: "rgba(255,255,255,0.02)", borderTop: "1px solid rgba(255,255,255,0.05)", fontSize: "0.85rem", color: "#a1a1aa" }}>
                        Showing {filteredMemories.length} of {memories.length} memories
                    </div>
                </div>
            )}
        </div>
    );
}
