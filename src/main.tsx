import React, { useState } from 'react';

export default function App() {
  // state to handle screen transitions: 'landing' or 'screening'
  const [currentScreen, setCurrentScreen] = useState<'landing' | 'screening'>('landing');

  return (
    <div className="min-h-screen bg-[#0B0F19] text-white overflow-hidden relative font-sans">
      {/* Background Glow matching your Figma cyber design */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(56,189,248,0.15),transparent_50%)] pointer-events-none" />

      {/* Navbar System */}
      <header className="relative z-10 flex items-center justify-between px-8 py-6 border-b border-white/10">
        <h1 className="text-2xl font-black tracking-widest text-cyan-400">IR</h1>

        <nav className="hidden md:flex gap-8 text-sm font-medium text-gray-400">
          <a href="#" className="text-cyan-400 font-semibold border-b-2 border-cyan-400 pb-1">
            Home
          </a>
          <a href="#" className="hover:text-cyan-400 transition pb-1">
            Features
          </a>
          <a href="#" className="hover:text-cyan-400 transition pb-1">
            Technology
          </a>
          <a href="#" className="hover:text-cyan-400 transition pb-1">
            Contact
          </a>
        </nav>

        <button className="px-5 py-2 rounded-full border border-cyan-400/50 text-cyan-400 hover:bg-cyan-400 hover:text-black hover:border-cyan-400 font-medium transition duration-300">
          Console V1.0
        </button>
      </header>

      {/* Conditional Screen Router Rendering */}
      {currentScreen === 'landing' ? (
        /* ================= SCREEN 1: FIGMA HERO LANDING ================= */
        <main className="relative z-10 flex flex-col items-center justify-center text-center px-6 h-[75vh]">
          <h2 className="max-w-5xl text-6xl md:text-8xl font-black leading-none tracking-tighter uppercase bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent drop-shadow-[0_0_35px_rgba(56,189,248,0.3)] animate-pulse">
            The Intelligent
            <br />
            Recruiter
          </h2>

          <p className="mt-6 text-gray-400 text-lg md:text-xl font-light tracking-wide max-w-2xl">
            AI-powered talent intelligence system for next-generation hiring
          </p>

          <div className="mt-12">
            <button 
              onClick={() => setCurrentScreen('screening')}
              className="px-10 py-4 text-md font-bold tracking-wider rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-[0_0_25px_rgba(6,182,212,0.4)] hover:shadow-[0_0_35px_rgba(6,182,212,0.6)] hover:scale-105 transition-all duration-300 active:scale-95"
            >
              START SCREENING
            </button>
          </div>
        </main>
      ) : (
        /* ================= SCREEN 2: CORE OPERATION MATRIX ================= */
        <main className="relative z-10 max-w-6xl mx-auto px-6 py-12">
          <div className="mb-8">
            <h2 className="text-3xl font-extrabold tracking-tight text-white">Target Profiling Console</h2>
            <p className="text-gray-400 mt-1">Configure parameters and upload bulk digital assets for AI processing pipelines.</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Left Operational Input Column */}
            <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6 shadow-xl">
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-cyan-400">
                <span>📝</span> Job Requirements Specification
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-xs uppercase tracking-wider text-gray-400 mb-2 font-semibold">Target Job Title</label>
                  <input 
                    type="text" 
                    placeholder="e.g., Data Analyst / Software Engineer" 
                    className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-cyan-400 transition"
                  />
                </div>
                
                <div>
                  <label className="block text-xs uppercase tracking-wider text-gray-400 mb-2 font-semibold">Required Technical Stacks & Competencies</label>
                  <textarea 
                    rows={6}
                    placeholder="e.g., Proficient with SQL schema queries, operational Git pipelines, Python data modules..." 
                    className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-cyan-400 transition resize-none"
                  />
                </div>
              </div>
            </div>

            {/* Right Operational Asset Upload Column */}
            <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6 shadow-xl flex flex-col justify-between">
              <div>
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-cyan-400">
                  <span>📂</span> Multi-Candidate Asset Deployment
                </h3>
                <p className="text-sm text-gray-400 mb-6">Please upload multiple candidate profiles simultaneously for batch matching sequence run.</p>
                
                {/* Drag and Drop Box Mock */}
                <div className="border-2 border-dashed border-white/20 hover:border-cyan-400/50 bg-black/20 rounded-2xl p-10 text-center cursor-pointer transition group">
                  <div className="text-4xl mb-3 group-hover:scale-110 transition duration-300">📥</div>
                  <p className="text-sm font-semibold text-gray-200">Drag & Drop candidate PDF resumes here</p>
                  <p className="text-xs text-gray-500 mt-1">Supports bulk PDF uploads</p>
                </div>
              </div>

              <div className="mt-8 pt-4 border-t border-white/5">
                <button className="w-full py-4 rounded-xl bg-cyan-400 text-black font-bold tracking-wider hover:bg-cyan-300 transition duration-300 shadow-lg">
                  RUN EVALUATION PIPELINE
                </button>
              </div>
            </div>
          </div>

          <div className="mt-6 text-center">
            <button 
              onClick={() => setCurrentScreen('landing')}
              className="text-sm text-gray-500 hover:text-gray-300 underline transition"
            >
              ↩ Return to Main Landing View
            </button>
          </div>
        </main>
      )}

      {/* Shared Footer Node */}
      <footer className="relative z-10 border-t border-white/10 py-8 text-center text-gray-600 text-xs tracking-wider uppercase">
        © 2026 Intelligent Recruiter Project Inc. All rights reserved.
      </footer>
    </div>
  );
}