export default function ApiKeysPage() {
    return (
        <div style={{ padding: "4rem", textAlign: "center" }}>
            <h1 className="neon-text" style={{ fontSize: "2rem", marginBottom: "1rem" }}>API Keys</h1>
            <p style={{ color: "#a1a1aa" }}>Manage your API keys for accessing Mem0 from external apps.</p>
            <div className="glass-card" style={{ maxWidth: "400px", margin: "2rem auto", padding: "1.5rem", borderRadius: "8px", textAlign: "left" }}>
                <p style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.5rem" }}>Default Key</p>
                <code style={{ background: "rgba(0,0,0,0.3)", padding: "4px 8px", borderRadius: "4px", color: "var(--primary)" }}>sk-mem0-local-dev-key</code>
            </div>
        </div>
    );
}
