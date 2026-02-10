import React, { useState } from 'react';
import { InputSection } from './components/InputSection';
import { FilterControls } from './components/FilterControls';
import { ResultsSection } from './components/ResultsSection';
import { extractEmails, processEmailList } from './utils/emailProcessor';
import { ProcessedDomain, ProcessingStats } from './types';
import { ShieldCheck } from 'lucide-react';

const DEFAULT_KEYWORDS = ['ceo', 'cfo', 'cto', 'founder', 'president', 'manager', 'director', 'vp', 'head', 'lead'];

const App: React.FC = () => {
  const [rawText, setRawText] = useState<string>('');
  const [keywords, setKeywords] = useState<string[]>(DEFAULT_KEYWORDS);
  const [maxPerDomain, setMaxPerDomain] = useState<number>(5);
  const [processedDomains, setProcessedDomains] = useState<ProcessedDomain[]>([]);
  const [stats, setStats] = useState<ProcessingStats | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [hasRun, setHasRun] = useState(false);

  const handleProcess = () => {
    if (!rawText.trim()) return;
    setIsProcessing(true);
    setHasRun(true);

    setTimeout(() => {
      const uniqueEmails = extractEmails(rawText);
      const result = processEmailList(uniqueEmails, keywords, maxPerDomain);
      
      setProcessedDomains(result.domains);
      setStats(result.stats);
      setIsProcessing(false);
    }, 100);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
              <ShieldCheck className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold text-gray-900 tracking-tight">AVANA Marketing</h1>
          </div>
          <div className="text-sm text-gray-500">Powered by Gemini AI</div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
              <p className="text-sm text-gray-500 mb-1">Detected Emails</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalEmailsFound}</p>
            </div>
            <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
              <p className="text-sm text-gray-500 mb-1">Unique Domains</p>
              <p className="text-2xl font-bold text-indigo-600">{stats.totalDomains}</p>
            </div>
            <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
              <p className="text-sm text-gray-500 mb-1">Final Selection</p>
              <p className="text-2xl font-bold text-green-600">{stats.totalSelected}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-4 space-y-8">
            <InputSection rawText={rawText} setRawText={setRawText} onProcess={handleProcess} />
            <FilterControls 
              keywords={keywords} 
              setKeywords={setKeywords} 
              maxPerDomain={maxPerDomain}
              setMaxPerDomain={setMaxPerDomain}
              onProcess={handleProcess}
              isProcessing={isProcessing}
            />
          </div>
          <div className="lg:col-span-8">
            <ResultsSection domains={processedDomains} hasRun={hasRun} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
