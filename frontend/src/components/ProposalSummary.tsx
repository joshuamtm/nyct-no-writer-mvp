import React from 'react';
import { Building2, DollarSign, Users, MapPin, Calendar, TrendingUp } from 'lucide-react';

export interface ExtractedProposalData {
  organizationName?: string;
  organizationMission?: string;
  foundingYear?: string;
  grantAmount?: string;
  projectDescription?: string;
  targetPopulation?: string;
  geographicScope?: string;
  currentBudget?: string;
  projectBudget?: string;
  peopleServed?: string;
  keyDeliverables?: string[];
  timeline?: string;
}

interface ProposalSummaryProps {
  summaryData: ExtractedProposalData;
  onProceed: () => void;
  onRegenerate: () => void;
  isLoading?: boolean;
}

const ProposalSummary: React.FC<ProposalSummaryProps> = ({
  summaryData,
  onProceed,
  onRegenerate,
  isLoading = false
}) => {
  if (isLoading) {
    return (
      <div className="p-6 bg-white rounded-lg">
        <div className="flex items-center justify-center space-x-2">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-500"></div>
          <span className="text-gray-600">Analyzing proposal...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg p-6 space-y-6">
      <div className="border-b pb-4">
        <h3 className="text-lg font-semibold text-navy-500 mb-2">Extracted Proposal Summary</h3>
        <p className="text-sm text-gray-600">
          Review the key information extracted from the proposal. This will be used to generate the decline memo.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {/* Organization Info */}
        <div className="space-y-3">
          <div className="flex items-start space-x-2">
            <Building2 className="h-5 w-5 text-primary-500 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-700">Organization</p>
              <p className="text-sm text-gray-900">{summaryData.organizationName || 'Not extracted'}</p>
            </div>
          </div>

          {summaryData.foundingYear && (
            <div className="flex items-start space-x-2">
              <Calendar className="h-5 w-5 text-primary-500 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-700">Founded</p>
                <p className="text-sm text-gray-900">{summaryData.foundingYear}</p>
              </div>
            </div>
          )}

          <div className="flex items-start space-x-2">
            <DollarSign className="h-5 w-5 text-primary-500 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-700">Grant Amount Requested</p>
              <p className="text-sm font-semibold text-gray-900">{summaryData.grantAmount || 'Not extracted'}</p>
            </div>
          </div>

          {summaryData.currentBudget && (
            <div className="flex items-start space-x-2">
              <TrendingUp className="h-5 w-5 text-primary-500 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-700">Current Operating Budget</p>
                <p className="text-sm text-gray-900">{summaryData.currentBudget}</p>
              </div>
            </div>
          )}
        </div>

        {/* Program Info */}
        <div className="space-y-3">
          <div className="flex items-start space-x-2">
            <Users className="h-5 w-5 text-primary-500 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-700">Target Population</p>
              <p className="text-sm text-gray-900">{summaryData.targetPopulation || 'Not extracted'}</p>
            </div>
          </div>

          <div className="flex items-start space-x-2">
            <MapPin className="h-5 w-5 text-primary-500 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-700">Geographic Scope</p>
              <p className="text-sm text-gray-900">{summaryData.geographicScope || 'Not extracted'}</p>
            </div>
          </div>

          {summaryData.peopleServed && (
            <div className="flex items-start space-x-2">
              <Users className="h-5 w-5 text-primary-500 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-700">People Served</p>
                <p className="text-sm text-gray-900">{summaryData.peopleServed}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Mission */}
      {summaryData.organizationMission && (
        <div className="border-t pt-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Organization Mission</p>
          <p className="text-sm text-gray-900">{summaryData.organizationMission}</p>
        </div>
      )}

      {/* Project Description */}
      <div className="border-t pt-4">
        <p className="text-sm font-medium text-gray-700 mb-2">Project Description</p>
        <p className="text-sm text-gray-900">
          {summaryData.projectDescription || 'No project description extracted'}
        </p>
      </div>

      {/* Key Deliverables */}
      {summaryData.keyDeliverables && summaryData.keyDeliverables.length > 0 && (
        <div className="border-t pt-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Key Deliverables</p>
          <ul className="list-disc list-inside text-sm text-gray-900 space-y-1">
            {summaryData.keyDeliverables.map((deliverable, index) => (
              <li key={index}>{deliverable}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex justify-between items-center pt-4 border-t">
        <button
          onClick={onRegenerate}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
        >
          Regenerate Summary
        </button>
        <button
          onClick={onProceed}
          className="px-6 py-2 text-sm font-medium text-white bg-primary-500 rounded-md hover:bg-primary-600 transition-colors"
        >
          Proceed to Generate Decline
        </button>
      </div>
    </div>
  );
};

export default ProposalSummary;