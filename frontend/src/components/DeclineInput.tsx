import React, { useState } from 'react';
import { AlertCircle, ChevronDown } from 'lucide-react';
import type { ExtractedProposalData } from './ProposalSummary';

interface DeclineInputProps {
  proposalSummary: ExtractedProposalData;
  onGenerate: (reasonCode: string, specificReasons: string) => void;
  isGenerating: boolean;
}

const DECLINE_REASONS = [
  { value: 'project_capability', label: 'Project Capability Problems' },
  { value: 'general_operating', label: 'General Operating Support' },
  { value: 'higher_merit', label: 'Other Projects Higher Merit' },
  { value: 'outside_guidelines', label: 'Outside Approved Guidelines' },
  { value: 'incomplete_proposal', label: 'Incomplete Proposal' },
  { value: 'geographic_scope', label: 'Geographic Scope Limitation' },
  { value: 'strategic_mismatch', label: 'Strategic Priority Mismatch' },
  { value: 'sustainability', label: 'Sustainability Concerns' }
];

const DeclineInput: React.FC<DeclineInputProps> = ({
  proposalSummary,
  onGenerate,
  isGenerating
}) => {
  const [selectedReason, setSelectedReason] = useState('');
  const [specificReasons, setSpecificReasons] = useState('');
  const [errors, setErrors] = useState<{ reason?: string; details?: string }>({});

  const handleGenerate = () => {
    const newErrors: { reason?: string; details?: string } = {};

    if (!selectedReason) {
      newErrors.reason = 'Please select a decline reason';
    }
    if (!specificReasons.trim()) {
      newErrors.details = 'Please provide specific reasons for the decline';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});
    onGenerate(selectedReason, specificReasons);
  };

  return (
    <div className="bg-white rounded-lg p-6 space-y-6">
      <div className="border-b pb-4">
        <h3 className="text-lg font-semibold text-navy-500 mb-2">Provide Decline Context</h3>
        <p className="text-sm text-gray-600">
          Based on the proposal analysis, select the primary decline reason and provide specific context.
        </p>
      </div>

      {/* Quick Summary Reference */}
      <div className="bg-softblue-50 p-4 rounded-lg">
        <p className="text-sm font-medium text-gray-700 mb-2">Proposal Quick Reference:</p>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>
            <span className="text-gray-600">Organization:</span>{' '}
            <span className="font-medium">{proposalSummary.organizationName}</span>
          </div>
          <div>
            <span className="text-gray-600">Amount:</span>{' '}
            <span className="font-medium">{proposalSummary.grantAmount}</span>
          </div>
          <div className="col-span-2">
            <span className="text-gray-600">Project:</span>{' '}
            <span className="font-medium">
              {proposalSummary.projectDescription?.substring(0, 100)}...
            </span>
          </div>
        </div>
      </div>

      {/* Decline Reason Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Board-Reportable Decline Reason <span className="text-red-500">*</span>
        </label>
        <div className="relative">
          <select
            value={selectedReason}
            onChange={(e) => {
              setSelectedReason(e.target.value);
              if (errors.reason) setErrors({ ...errors, reason: undefined });
            }}
            className={`w-full px-4 py-2 pr-10 border rounded-md appearance-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
              errors.reason ? 'border-red-500' : 'border-gray-300'
            }`}
          >
            <option value="">Select a decline reason...</option>
            {DECLINE_REASONS.map((reason) => (
              <option key={reason.value} value={reason.value}>
                {reason.label}
              </option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
        </div>
        {errors.reason && (
          <p className="mt-1 text-sm text-red-600 flex items-center">
            <AlertCircle className="h-4 w-4 mr-1" />
            {errors.reason}
          </p>
        )}
      </div>

      {/* Specific Reasons Input */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Specific Decline Reasons <span className="text-red-500">*</span>
        </label>
        <p className="text-xs text-gray-600 mb-2">
          Provide 3-4 specific, factual reasons why this proposal doesn't meet NYCT's criteria. 
          Reference concrete details from the proposal (budget concerns, capacity issues, strategic misalignment, etc.)
        </p>
        <textarea
          value={specificReasons}
          onChange={(e) => {
            setSpecificReasons(e.target.value);
            if (errors.details) setErrors({ ...errors, details: undefined });
          }}
          className={`w-full px-4 py-3 border rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
            errors.details ? 'border-red-500' : 'border-gray-300'
          }`}
          rows={6}
          placeholder="Example: The organization's FY25 budget is more than double their current operating budget and relies almost exclusively on community donations. The proposal does not provide strong evidence that they can manage the increased operational demands. The organization employs only five part-time staff and uses volunteers for most programming..."
          maxLength={1000}
        />
        <div className="flex justify-between items-center mt-1">
          <div>
            {errors.details && (
              <p className="text-sm text-red-600 flex items-center">
                <AlertCircle className="h-4 w-4 mr-1" />
                {errors.details}
              </p>
            )}
          </div>
          <span className="text-xs text-gray-500">
            {specificReasons.length}/1000 characters
          </span>
        </div>
      </div>

      {/* Guidance Box */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-start">
          <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5 mr-2 flex-shrink-0" />
          <div className="text-sm text-yellow-800">
            <p className="font-medium mb-1">Writing Effective Decline Reasons:</p>
            <ul className="list-disc list-inside space-y-1 text-xs">
              <li>Be specific and factual - avoid generic statements</li>
              <li>Reference concrete numbers from the proposal (budget, staffing, etc.)</li>
              <li>Focus on programmatic or capacity issues, not organizational character</li>
              <li>Ensure reasons align with the selected board-reportable category</li>
              <li>The final memo should be readable in 5 minutes without the original proposal</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Generate Button */}
      <div className="flex justify-end pt-4 border-t">
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className={`px-6 py-2 text-sm font-medium text-white rounded-md transition-colors ${
            isGenerating
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-primary-500 hover:bg-primary-600'
          }`}
        >
          {isGenerating ? (
            <span className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"></div>
              Generating Decline Memo...
            </span>
          ) : (
            'Generate Decline Memo'
          )}
        </button>
      </div>
    </div>
  );
};

export default DeclineInput;