import { useState } from 'react';
import FileUpload from './components/FileUpload';
import ProposalSummary from './components/ProposalSummary';
import type { ExtractedProposalData } from './components/ProposalSummary';
import DeclineInput from './components/DeclineInput';
import OutputPanel from './components/OutputPanel';
import MetricsPanel from './components/MetricsPanel';
import { Upload, MessageSquare, Zap, BarChart3, CheckCircle2, ArrowRight, FileSearch } from 'lucide-react';
import { API_URL, ANALYZE_URL, GENERATE_URL } from './config';

export interface ReasonCode {
  value: string;
  label: string;
}

export interface GeneratedOutput {
  internal_rationale: string;
  external_reply: string;
  generation_time_ms: number;
}

export interface UploadedFile {
  proposal_hash: string;
  text_content: string;
  filename: string;
  size: number;
}

function App() {
  const [currentStage, setCurrentStage] = useState<'upload' | 'analysis' | 'decline' | 'output'>('upload');
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [proposalSummary, setProposalSummary] = useState<ExtractedProposalData | null>(null);
  const [generatedOutput, setGeneratedOutput] = useState<GeneratedOutput | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [showMetrics, setShowMetrics] = useState<boolean>(false);

  // Debug logging
  console.log('App component loaded successfully - Two-Stage Version');

  const handleFileUploaded = async (file: UploadedFile | null) => {
    if (!file) return;
    
    setUploadedFile(file);
    setCurrentStage('analysis');
    setIsAnalyzing(true);

    try {
      // Call backend to analyze proposal
      const response = await fetch(ANALYZE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          proposal_hash: file.proposal_hash,
          text_content: file.text_content,
          filename: file.filename
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze proposal');
      }

      const data = await response.json();
      
      // Use the actual data from the API
      if (data.summary) {
        setProposalSummary(data.summary);
      } else {
        // Only use basic fallback if API returns no summary
        const fallbackSummary: ExtractedProposalData = {
          organizationName: extractOrganizationName(file.text_content) || 'Organization',
          grantAmount: extractGrantAmount(file.text_content) || 'Amount not specified',
          projectDescription: file.text_content.substring(0, 200) || 'Project description',
          targetPopulation: 'Community members',
          geographicScope: 'Local area'
        };
        setProposalSummary(fallbackSummary);
      }
    } catch (error) {
      console.error('Error analyzing proposal:', error);
      // Show error but still try to extract basic info
      alert('Note: Using basic text extraction. For full AI analysis, ensure Supabase functions are configured.');
      const basicSummary: ExtractedProposalData = {
        organizationName: extractOrganizationName(file.text_content) || 'Organization',
        grantAmount: extractGrantAmount(file.text_content) || 'Funding amount not specified',
        projectDescription: file.text_content.substring(0, 300) || 'See uploaded document',
        targetPopulation: 'See proposal details',
        geographicScope: 'See proposal details'
      };
      setProposalSummary(basicSummary);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Helper functions to extract key information from text
  const extractOrganizationName = (text: string): string | undefined => {
    // Simple extraction logic - can be enhanced
    const lines = text.split('\n');
    for (const line of lines) {
      if (line.includes('Organization:') || line.includes('Applicant:')) {
        return line.split(':')[1]?.trim();
      }
    }
    return undefined;
  };

  const extractGrantAmount = (text: string): string | undefined => {
    // Look for dollar amounts
    const amountMatch = text.match(/\$[\d,]+(?:\.\d{2})?/);
    return amountMatch ? amountMatch[0] : undefined;
  };

  const extractFoundingYear = (text: string): string | undefined => {
    // Look for founding year patterns
    const yearMatch = text.match(/founded in (\d{4})|established (\d{4})|since (\d{4})/i);
    return yearMatch ? (yearMatch[1] || yearMatch[2] || yearMatch[3]) : undefined;
  };

  const extractProjectDescription = (text: string): string | undefined => {
    // Extract first substantial paragraph as project description
    const paragraphs = text.split('\n\n').filter(p => p.length > 100);
    return paragraphs[0]?.substring(0, 300);
  };

  const handleProceedToDecline = () => {
    setCurrentStage('decline');
  };

  const handleRegenerateSummary = () => {
    if (uploadedFile) {
      handleFileUploaded(uploadedFile);
    }
  };

  const handleGenerateDecline = async (reasonCode: string, specificReasons: string) => {
    if (!proposalSummary) return;

    setIsGenerating(true);
    try {
      // Generate NYCT-formatted internal memo
      const internalMemo = generateNYCTFormattedMemo(proposalSummary, reasonCode, specificReasons);
      
      // Generate generic external letter
      const externalLetter = generateExternalLetter(reasonCode);

      const output: GeneratedOutput = {
        internal_rationale: internalMemo,
        external_reply: externalLetter,
        generation_time_ms: 2000
      };

      setGeneratedOutput(output);
      setCurrentStage('output');
    } catch (error) {
      console.error('Error generating decline:', error);
      alert('Error generating decline memo. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateNYCTFormattedMemo = (
    summary: ExtractedProposalData,
    reasonCode: string,
    specificReasons: string
  ): string => {
    const reasonLabels: Record<string, string> = {
      'project_capability': 'Project Capability Problems',
      'general_operating': 'General Operating Support',
      'higher_merit': 'Other Projects Higher Merit',
      'outside_guidelines': 'Outside Approved Guidelines',
      'incomplete_proposal': 'Incomplete Proposal',
      'geographic_scope': 'Geographic Scope Limitation',
      'strategic_mismatch': 'Strategic Priority Mismatch',
      'sustainability': 'Sustainability Concerns'
    };

    return `${summary.organizationName}${summary.foundingYear ? `, founded in ${summary.foundingYear},` : ''} ${summary.organizationMission || 'serves the community'}. This ${summary.grantAmount} request is to support ${summary.projectDescription}. ${summary.projectBudget ? `The project budget is ${summary.projectBudget}` : ''}${summary.currentBudget ? ` and the organization's current operating budget is ${summary.currentBudget}.` : '.'}

I recommend this request be declined for ${reasonLabels[reasonCode]?.toLowerCase() || 'the selected reason'}. ${specificReasons}

Rationale: ${reasonLabels[reasonCode] || 'Decline Reason'}`;
  };

  const generateExternalLetter = (_reasonCode: string): string => {
    return `Dear Applicant,

Thank you for your proposal submission to The New York Community Trust. We genuinely appreciate your organization's dedication to serving the community and the considerable time you invested in preparing your application.

After careful review by our program team and board, we have determined that we will not be able to provide funding for this request at this time. While we recognize the important work your organization does, this proposal does not align with our current funding priorities.

We encourage you to review our updated funding guidelines on our website and invite you to consider applying for future opportunities that may better align with your organization's mission and our strategic priorities.

Thank you again for considering The New York Community Trust as a potential partner in your work.

Best regards,
NYCT Program Team`;
  };

  const resetForm = () => {
    setUploadedFile(null);
    setProposalSummary(null);
    setGeneratedOutput(null);
    setCurrentStage('upload');
  };

  // Progress steps for the two-stage process
  const getProgressStep = () => {
    switch (currentStage) {
      case 'upload': return 1;
      case 'analysis': return 2;
      case 'decline': return 3;
      case 'output': return 4;
      default: return 1;
    }
  };

  const progressStep = getProgressStep();
  const steps = [
    { id: 1, title: 'Upload Proposal', icon: Upload, completed: currentStage !== 'upload' },
    { id: 2, title: 'Review Analysis', icon: FileSearch, completed: currentStage === 'decline' || currentStage === 'output' },
    { id: 3, title: 'Add Context', icon: MessageSquare, completed: currentStage === 'output' },
    { id: 4, title: 'Generate Memo', icon: Zap, completed: !!generatedOutput }
  ];

  return (
    <div className="min-h-screen bg-bgwhite flex flex-col">
      {/* MTM Header */}
      <header className="bg-cream shadow-sm border-b sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center py-4 sm:py-6 space-y-3 sm:space-y-0">
            <div className="flex items-center space-x-4">
              <img 
                src="/mtm-logo.png" 
                alt="Meet the Moment" 
                className="h-[60px] w-auto"
                onError={(e) => {
                  console.error('Failed to load MTM logo');
                  e.currentTarget.style.display = 'none';
                }}
              />
              <div className="border-l-2 border-softblue-400 pl-4">
                <h1 className="text-2xl font-bold text-navy-500">NYCT No-Writer</h1>
                <p className="text-gray-600 text-sm">Two-Stage Decline Memo Generator</p>
              </div>
            </div>
            <button
              onClick={() => setShowMetrics(!showMetrics)}
              className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-navy-500 bg-softblue-100 rounded-md hover:bg-softblue-200 transition-colors"
            >
              <BarChart3 className="h-4 w-4" />
              <span>Analytics</span>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 flex-grow">
        {/* Step Progress Indicator */}
        <div className="mb-6 sm:mb-8" role="navigation" aria-label="Progress indicator">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 space-y-2 sm:space-y-0">
            <h2 className="text-lg font-semibold text-slate-900">
              Step {progressStep} of {steps.length}
            </h2>
            <span className="text-sm text-slate-600" aria-live="polite">
              {Math.round((steps.filter(s => s.completed).length / steps.length) * 100)}% Complete
            </span>
          </div>
          
          <div className="flex items-center space-x-1 sm:space-x-2 mb-6 overflow-x-auto pb-2">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center flex-1 min-w-0">
                <div 
                  className={`flex items-center justify-center w-8 h-8 rounded-full border-2 transition-all duration-200 flex-shrink-0 ${
                    step.completed 
                      ? 'bg-accent-100 border-accent-500 text-accent-600'
                      : progressStep === step.id
                      ? 'bg-primary-100 border-primary-500 text-primary-600'
                      : 'bg-softblue-100 border-softblue-400 text-softblue-500'
                  }`}
                  role="progressbar"
                  aria-valuenow={step.completed ? 100 : progressStep === step.id ? 50 : 0}
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-label={`${step.title} ${step.completed ? 'completed' : progressStep === step.id ? 'in progress' : 'not started'}`}
                >
                  {step.completed ? (
                    <CheckCircle2 className="h-4 w-4 sm:h-5 sm:w-5" />
                  ) : (
                    <span className="text-xs sm:text-sm font-semibold">{step.id}</span>
                  )}
                </div>
                {index < steps.length - 1 && (
                  <div className={`flex-1 h-0.5 mx-1 sm:mx-2 transition-colors duration-200 min-w-4 ${
                    step.completed ? 'bg-accent-500' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>

          <div className="text-center">
            <h3 className="text-lg sm:text-xl font-bold text-navy-500 mb-2">
              {progressStep <= 4 ? steps[progressStep - 1].title : 'Complete'}
            </h3>
            <p className="text-sm sm:text-base text-gray-600">
              {currentStage === 'upload' && 'Upload your grant proposal document to begin the analysis'}
              {currentStage === 'analysis' && 'Review the extracted information from the proposal'}
              {currentStage === 'decline' && 'Provide specific context for the decline decision'}
              {currentStage === 'output' && 'Review and use your generated decline memo'}
            </p>
          </div>
        </div>

        {showMetrics && (
          <div className="mb-8">
            <MetricsPanel />
          </div>
        )}

        {/* Stage Content */}
        <div className="space-y-6 sm:space-y-8">
          {/* Stage 1: Upload */}
          {currentStage === 'upload' && (
            <section 
              className="bg-white rounded-lg shadow-card border border-gray-200 p-4 sm:p-6 ring-2 ring-primary-500 ring-opacity-20"
              aria-labelledby="upload-heading"
            >
              <div className="flex items-center mb-4">
                <Upload className="h-5 w-5 text-primary-500 mr-2 flex-shrink-0" />
                <h3 id="upload-heading" className="text-base sm:text-lg font-semibold text-navy-500">Upload Grant Proposal</h3>
              </div>
              <FileUpload
                onFileUploaded={handleFileUploaded}
                uploadedFile={uploadedFile}
              />
            </section>
          )}

          {/* Stage 2: Analysis Review */}
          {currentStage === 'analysis' && (
            <section 
              className="bg-white rounded-lg shadow-card border border-gray-200 p-4 sm:p-6 ring-2 ring-primary-500 ring-opacity-20"
              aria-labelledby="analysis-heading"
            >
              <div className="flex items-center mb-4">
                <FileSearch className="h-5 w-5 text-primary-500 mr-2 flex-shrink-0" />
                <h3 id="analysis-heading" className="text-base sm:text-lg font-semibold text-navy-500">Proposal Analysis</h3>
              </div>
              {proposalSummary ? (
                <ProposalSummary
                  summaryData={proposalSummary}
                  onProceed={handleProceedToDecline}
                  onRegenerate={handleRegenerateSummary}
                  isLoading={isAnalyzing}
                />
              ) : (
                <div className="flex items-center justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-500"></div>
                  <span className="ml-3 text-gray-600">Analyzing proposal...</span>
                </div>
              )}
            </section>
          )}

          {/* Stage 3: Decline Input */}
          {currentStage === 'decline' && proposalSummary && (
            <section 
              className="bg-white rounded-lg shadow-card border border-gray-200 p-4 sm:p-6 ring-2 ring-primary-500 ring-opacity-20"
              aria-labelledby="decline-heading"
            >
              <div className="flex items-center mb-4">
                <MessageSquare className="h-5 w-5 text-primary-500 mr-2 flex-shrink-0" />
                <h3 id="decline-heading" className="text-base sm:text-lg font-semibold text-navy-500">Decline Context</h3>
              </div>
              <DeclineInput
                proposalSummary={proposalSummary}
                onGenerate={handleGenerateDecline}
                isGenerating={isGenerating}
              />
            </section>
          )}

          {/* Stage 4: Output */}
          {currentStage === 'output' && generatedOutput && (
            <section 
              className="bg-white rounded-lg shadow-card border border-gray-200 p-4 sm:p-6"
              aria-labelledby="output-heading"
            >
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-3 sm:space-y-0">
                <div className="flex items-center">
                  <CheckCircle2 className="h-5 w-5 text-accent-500 mr-2 flex-shrink-0" />
                  <h3 id="output-heading" className="text-base sm:text-lg font-semibold text-navy-500">Generated Decline Memo</h3>
                </div>
                <button
                  onClick={resetForm}
                  className="flex items-center justify-center space-x-2 px-4 py-2 text-sm font-medium text-navy-500 bg-softblue-100 rounded-md hover:bg-softblue-200 transition-colors min-h-[44px]"
                  aria-label="Start a new decline process"
                >
                  <ArrowRight className="h-4 w-4" />
                  <span>Start New Process</span>
                </button>
              </div>
              <OutputPanel output={generatedOutput} />
            </section>
          )}
        </div>
      </main>

      {/* MTM Footer */}
      <footer className="bg-cream text-center py-6 px-4 mt-12">
        <img 
          src="/mtm-logo.png" 
          alt="Meet the Moment" 
          className="h-10 mx-auto mb-2"
          onError={(e) => {
            console.error('Failed to load MTM footer logo');
            e.currentTarget.style.display = 'none';
          }}
        />
        <p className="text-gray-600 text-sm">Prototype by Meet the Moment</p>
      </footer>
    </div>
  );
}

export default App;