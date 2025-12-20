"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import {
  Search, ExternalLink, Newspaper, Zap,
  LayoutGrid, Trophy, Cpu, Film, Briefcase, Plus,
  HeartPulse, Globe, Landmark, MapPin, ChevronRight
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

// 1. Category Definitions (Preserved)
const CATEGORIES = [
  { id: "all", label: "Top Stories", icon: LayoutGrid },
  { id: "india", label: "India", icon: MapPin },
  { id: "world", label: "World", icon: Globe },
  { id: "politics", label: "Politics", icon: Landmark },
  { id: "business", label: "Finance", icon: Briefcase },
  { id: "technology", label: "Tech", icon: Cpu },
  { id: "health", label: "Health", icon: HeartPulse },
  { id: "sports", label: "Sports", icon: Trophy },
  { id: "entertainment", label: "Cinema", icon: Film },
];

// 2. Robust Image Component (Re-styled for Isometric Card)
const NewsImage = ({ src, alt }: { src: string; alt: string }) => {
  const [imgSrc, setImgSrc] = useState(src);
  const [error, setError] = useState(false);
  const fallback = "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1000&auto=format&fit=crop";

  return (
    <div className="relative w-full h-56 lg:h-full overflow-hidden rounded-t-3xl lg:rounded-l-3xl lg:rounded-tr-none z-10">
      <div className="absolute inset-0 bg-gradient-to-t from-[#151520] via-transparent to-transparent z-20" />
      <div className="absolute inset-0 bg-accent-red/10 mix-blend-overlay z-20" />
      <img
        src={imgSrc || fallback}
        alt={alt}
        className={`w-full h-full object-cover transition-all duration-700 group-hover:scale-110 ${error ? 'opacity-50 grayscale' : 'opacity-90'}`}
        onError={() => {
          setImgSrc(fallback);
          setError(true);
        }}
      />
       <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-[#151520] to-transparent z-20" />
    </div>
  );
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState("all");
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [feed, setFeed] = useState<any[]>([]);

  // 3. Unified Fetch Logic (Functionality Preserved)
  const fetchNews = async (isNewSearch = false, category = activeCategory, searchOverride = "") => {
    setLoading(true);
    const currentPage = isNewSearch ? 1 : page;

    try {
      // Ensure your backend is running on 127.0.0.1:5000
      const res = await axios.get("http://127.0.0.1:5000/api/feed", {
        params: {
          category: searchOverride ? "" : category,
          query: searchOverride,
          page: currentPage
        }
      });

      const newItems = res.data.feed || [];
      setFeed(prev => isNewSearch ? newItems : [...prev, ...newItems]);
      if (!isNewSearch) setPage(currentPage + 1);
    } catch (error) {
      console.error("Feed Error:", error);
    } finally {
      setLoading(false);
    }
  };

  // 4. Initial Load & Category Switch (Functionality Preserved)
  useEffect(() => {
    setPage(1);
    fetchNews(true, activeCategory);
  }, [activeCategory]);

  const handleSearch = () => {
    if (!query) return;
    setActiveCategory("");
    fetchNews(true, "", query);
  };

  return (
    <div className="min-h-screen isometric-bg text-white p-6 md:p-12 overflow-x-hidden relative">
      
      <div className="relative z-10 max-w-7xl mx-auto">
        {/* NAVIGATION BAR */}
        <nav className="flex flex-col md:flex-row items-center justify-between mb-16 gap-8">
            <div className="flex items-center gap-4 cursor-pointer group">
                <div className="relative">
                    <div className="absolute inset-0 bg-accent-red blur-lg opacity-40 group-hover:opacity-70 transition-opacity"></div>
                    <div className="relative w-12 h-12 bg-gradient-to-br from-accent-red to-[#a12323] rounded-xl flex items-center justify-center shadow-lg shadow-accent-red/30 border border-accent-red/20 transform -skew-x-6">
                        <Zap className="text-white w-6 h-6 fill-current group-hover:scale-110 transition-transform" />
                    </div>
                </div>
                <div>
                    <h1 className="text-3xl font-black tracking-tighter leading-none">SIGMA<span className="text-accent-red">NEWS</span></h1>
                    <p className="text-[10px] font-bold text-gray-400 tracking-[0.4em] uppercase ml-0.5">Neural Ingestion Mesh</p>
                </div>
            </div>

            <div className="relative w-full md:w-[450px] group">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-accent-red/0 via-accent-red/30 to-accent-red/0 rounded-xl blur-md opacity-0 group-focus-within:opacity-100 transition-opacity duration-500"></div>
                <input
                    type="text"
                    placeholder="Search deep intel..."
                    className="relative w-full bg-[#151520] border border-white/10 rounded-xl p-4 pl-12 text-sm focus:border-accent-red/50 focus:ring-1 focus:ring-accent-red/20 outline-none transition-all text-white placeholder:text-gray-500 shadow-[inset_0_2px_10px_#000] transform -skew-x-3"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                />
                <Search className="absolute left-4 top-4 text-gray-500 w-5 h-5 group-focus-within:text-accent-red transition-colors z-20" />
            </div>
        </nav>

        {/* NEW HERO SECTION (Inspired by Reference Image) */}
        <section className="flex flex-col md:flex-row items-center justify-between mb-24 iso-perspective">
            <div className="md:w-1/2 mb-12 md:mb-0 z-10">
                <h1 className="text-5xl md:text-7xl font-black leading-tight mb-6">
                    Neural <br/>
                    <span className="text-accent-red">News Ingestion</span> <br/>
                    System.
                </h1>
                <p className="text-gray-400 text-lg mb-8 max-w-md">
                    Real-time AI processing and isometric visualization of global intelligence streams.
                </p>
                <button onClick={() => handleSearch()} className="group relative inline-flex items-center gap-3 bg-accent-red text-white px-8 py-4 rounded-xl font-bold text-sm overflow-hidden transform hover:-translate-y-1 transition-all shadow-lg shadow-accent-red/30">
                    <span className="relative z-10 flex items-center">Example Search <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" /></span>
                    <div className="absolute inset-0 bg-white/20 skew-x-12 -translate-x-full group-hover:translate-x-0 transition-transform duration-700"></div>
                </button>
            </div>
            
            {/* Placeholder for Isometric Hero Image - Replace with your own */}
            <div className="md:w-1/2 relative">
                <div className="w-full h-[400px] relative">
                    {/* Abstract Isometric Shapes representing data/server */}
                    <div className="absolute top-10 right-10 w-64 h-64 bg-gradient-to-br from-accent-red/20 to-transparent rounded-3xl transform rotate-45 skew-x-12 blur-xl animate-pulse"></div>
                    <div className="absolute top-20 right-20 w-48 h-48 bg-[#1a1a28] border border-accent-red/30 rounded-3xl transform rotate-[30deg] skew-x-[20deg] shadow-2xl shadow-accent-red/10">
                        <div className="absolute inset-0 bg-gradient-to-br from-transparent to-accent-red/5 rounded-3xl"></div>
                    </div>
                     <div className="absolute top-0 right-0 w-56 h-56 bg-[#151520] border-2 border-accent-red rounded-3xl transform rotate-[60deg] skew-x-[30deg] shadow-[0_20px_50px_rgba(255,62,62,0.2)] flex items-center justify-center">
                        <Zap className="w-20 h-20 text-accent-red fill-current opacity-80" />
                    </div>
                </div>
            </div>
        </section>

        {/* CATEGORY SELECTOR */}
        <div className="mb-16">
            <div className="flex gap-4 overflow-x-auto pb-6 no-scrollbar p-1">
                {CATEGORIES.map((cat) => (
                    <button
                        key={cat.id}
                        onClick={() => setActiveCategory(cat.id)}
                        className={`relative flex items-center gap-3 px-6 py-3 rounded-xl text-sm font-bold transition-all whitespace-nowrap overflow-hidden transform skew-x-[-6deg] ${
                            activeCategory === cat.id
                            ? "bg-accent-red text-white shadow-lg shadow-accent-red/30"
                            : "bg-[#151520] text-gray-400 border border-white/5 hover:border-accent-red/30 hover:text-white"
                        }`}
                    >
                        <cat.icon className={`w-4 h-4 relative z-10 ${activeCategory === cat.id ? 'text-white' : ''}`} />
                        <span className="relative z-10">{cat.label}</span>
                        {activeCategory === cat.id && (
                            <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent z-0"></div>
                        )}
                    </button>
                ))}
            </div>
        </div>

        {/* MAIN CONTENT FEED - ISOMETRIC CARDS */}
        <main className="min-h-[50vh] iso-perspective">
            <div className="grid grid-cols-1 gap-12">
                <AnimatePresence mode="popLayout">
                    {feed.map((item, idx) => {
                        const validFacts = item.facts?.filter((f: any) => f.actor && f.action) || [];

                        return (
                            <motion.div
                                key={`${item.url}-${idx}`}
                                initial={{ opacity: 0, y: 100, rotateX: 20, scale: 0.9 }}
                                whileInView={{ opacity: 1, y: 0, rotateX: 0, scale: 1 }}
                                viewport={{ once: true, margin: "-50px" }}
                                transition={{ type: "spring", bounce: 0.3, duration: 0.8, delay: idx * 0.05 }}
                                whileHover={{ 
                                    y: -15, 
                                    rotateX: 10, 
                                    scale: 1.02,
                                    boxShadow: "0 30px 60px -15px rgba(0, 0, 0, 0.5), 0 0 40px rgba(255, 62, 62, 0.15)"
                                }}
                                style={{ transformStyle: "preserve-3d" }}
                                className="group relative bg-[#151520] rounded-3xl overflow-hidden flex flex-col lg:flex-row min-h-[400px] border border-white/5 shadow-2xl"
                            >
                                {/* ACCENT BORDER */}
                                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-accent-red via-transparent to-accent-red opacity-50"></div>

                                {/* MEDIA SECTION */}
                                <div className="lg:w-2/5 relative">
                                    <NewsImage src={item.image} alt={item.title} />
                                    <div className="absolute top-6 left-6 bg-[#0a0a12]/80 backdrop-blur-md border border-accent-red/30 px-4 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest text-white z-20 shadow-lg transform -skew-x-6">
                                        <span className="text-accent-red mr-1">SOURCE:</span> {item.source}
                                    </div>
                                </div>

                                {/* TEXT SECTION */}
                                <div className="lg:w-3/5 p-8 lg:p-10 flex flex-col relative">
                                    
                                    <h2 className="text-2xl lg:text-3xl font-black mb-6 leading-tight text-white group-hover:text-accent-red transition-colors">
                                        {item.title}
                                    </h2>

                                    <p className="text-gray-400 text-sm lg:text-base leading-relaxed mb-8 pl-4 border-l-2 border-accent-red/50 line-clamp-3 group-hover:line-clamp-none transition-all">
                                        {item.summary}
                                    </p>

                                    {/* KEY FACTS - ISOMETRIC DATA BLOCK */}
                                    {validFacts.length > 0 && (
                                        <div className="mb-6 bg-[#0a0a12] p-5 rounded-2xl border border-white/5 relative overflow-hidden shadow-inner transform skew-x-[-2deg]">
                                             <div className="absolute inset-0 bg-[linear-gradient(to_bottom,transparent_2px,#ff3e3e_2px)] bg-[size:100%_4px] opacity-[0.03] pointer-events-none"></div>
                                            
                                            <h3 className="text-[10px] font-bold text-accent-red uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
                                                <Newspaper className="w-3 h-3" /> Intel Extraction
                                            </h3>

                                            <div className="grid grid-cols-1 gap-3 relative z-10">
                                                {validFacts.slice(0, 2).map((f: any, i: number) => (
                                                    <div key={i} className="flex items-start gap-3 p-3 bg-[#151520] rounded-lg border border-white/5">
                                                        <div className="mt-1.5 w-2 h-2 rounded-sm bg-accent-red shrink-0 shadow-[0_0_10px_rgba(255,62,62,0.8)]" />
                                                        <p className="text-xs text-gray-300 leading-relaxed">
                                                            <span className="text-white font-bold">{f.actor}</span> <span className="text-accent-red/80 mx-0.5">{f.action}</span> <span className="text-gray-400 font-medium">{f.object}</span>
                                                        </p>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    <div className="flex items-center justify-between mt-auto pt-4 border-t border-white/5">
                                        <a href={item.url} target="_blank" className="group/link flex items-center gap-2 text-xs font-black text-accent-red hover:text-white transition-all uppercase tracking-widest">
                                            Verify Source <ExternalLink className="w-3 h-3 group-hover/link:translate-x-1 group-hover/link:-translate-y-1 transition-transform" />
                                        </a>
                                        <Zap className={`w-5 h-5 ${loading ? 'animate-pulse text-accent-red' : 'text-gray-600 group-hover:text-accent-red transition-colors'}`} />
                                    </div>
                                </div>
                            </motion.div>
                        );
                    })}
                </AnimatePresence>
            </div>

            {/* LOADING & LOAD MORE */}
            <div className="mt-20 pb-20 flex flex-col items-center gap-6 relative z-10">
                {loading && (
                    <div className="flex items-center gap-3 text-accent-red font-bold animate-pulse tracking-widest uppercase text-xs">
                        <Zap className="w-4 h-4" />
                        Processing Neural Feed...
                    </div>
                )}

                {!loading && feed.length > 0 && (
                    <button
                        onClick={() => fetchNews(false)}
                        className="group relative overflow-hidden bg-accent-red hover:bg-[#d12c2c] text-white px-12 py-4 rounded-xl font-black text-sm transition-all shadow-lg shadow-accent-red/30 flex items-center gap-3 transform skew-x-[-6deg] hover:-translate-y-1"
                    >
                        <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.2)_50%,transparent_75%)] bg-[length:250%_250%,100%_100%] animate-[shimmer_2s_linear_infinite] pointer-events-none"></div>
                        <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform relative z-10" />
                        <span className="relative z-10">LOAD MORE INTEL</span>
                    </button>
                )}
            </div>
        </main>

        <footer className="max-w-7xl mx-auto mt-20 pb-12 border-t border-white/5 pt-8 text-center relative z-10">
            <p className="text-[10px] font-bold text-gray-500 tracking-[0.5em] uppercase">Sigma OS • Isometric Ingestion v4.0 • System Ready</p>
        </footer>
      </div>
    </div>
  );
}