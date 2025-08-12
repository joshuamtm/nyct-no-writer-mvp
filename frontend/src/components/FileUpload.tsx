import React, { useCallback, useState } from 'react';
import { Upload, CheckCircle, AlertCircle, X } from 'lucide-react';
import type { UploadedFile } from '../App';

interface FileUploadProps {
  onFileUploaded: (file: UploadedFile | null) => void;
  uploadedFile: UploadedFile | null;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUploaded, uploadedFile }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleFileUpload = useCallback(async (file: File) => {
    setError('');
    setIsUploading(true);

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      setError('File too large. Maximum size is 10MB.');
      setIsUploading(false);
      return;
    }

    // Validate file type
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain',  // Allow text files for testing
      'application/msword'
    ];
    
    // Allow text files or if no type detected (some browsers)
    if (!allowedTypes.includes(file.type) && file.type !== '') {
      setError('Only PDF, Word documents, and text files are allowed.');
      setIsUploading(false);
      return;
    }

    try {
      // Read actual file content
      let fileContent = '';
      
      if (file.type === 'application/pdf') {
        // For PDF files, we'll pass them through as-is
        // The backend or Supabase function will handle extraction
        fileContent = `[PDF File: ${file.name}] - Content will be extracted by backend`;
      } else {
        // For text-based files, read the content
        fileContent = await file.text();
      }
      
      // Create the uploaded file object with real content
      const uploadedFile: UploadedFile = {
        proposal_hash: Math.random().toString(36).substring(7),
        text_content: fileContent || `Content from ${file.name}`,
        filename: file.name,
        size: file.size
      };

      onFileUploaded(uploadedFile);
    } catch (error) {
      console.error('Upload error:', error);
      setError('Failed to upload file. Please try again.');
    } finally {
      setIsUploading(false);
    }
  }, [onFileUploaded]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, [handleFileUpload]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  }, [handleFileUpload]);

  const clearFile = () => {
    onFileUploaded(null);
    setError('');
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (uploadedFile) {
    return (
      <div className="border-2 border-accent-300 border-dashed rounded-lg p-4 bg-accent-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-accent-100 p-2 rounded-full">
              <CheckCircle className="h-5 w-5 text-accent-600" />
            </div>
            <div>
              <p className="font-medium text-navy-500">{uploadedFile.filename}</p>
              <p className="text-sm text-gray-600">
                {formatFileSize(uploadedFile.size)} • Ready for processing
              </p>
            </div>
          </div>
          <button
            onClick={clearFile}
            className="p-2 text-accent-600 hover:text-accent-700 hover:bg-accent-100 rounded-md transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div
        className={`
          border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all duration-200
          ${isDragOver
            ? 'border-primary-400 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
          }
          ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isUploading && document.getElementById('file-input')?.click()}
      >
        <input
          id="file-input"
          type="file"
          className="hidden"
          accept=".pdf,.docx,.txt,.doc"
          onChange={handleFileSelect}
          disabled={isUploading}
        />
        
        {isUploading ? (
          <div className="flex flex-col items-center space-y-3">
            <div className="animate-spin rounded-full h-8 w-8 border-2 border-gray-200 border-t-primary-500"></div>
            <div>
              <p className="text-gray-900 font-medium">Processing your document...</p>
              <p className="text-sm text-gray-600">This may take a few seconds</p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className={`p-3 rounded-full w-fit mx-auto ${
              isDragOver ? 'bg-primary-100' : 'bg-softblue-100'
            }`}>
              <Upload className={`h-8 w-8 ${
                isDragOver ? 'text-primary-600' : 'text-softblue-400'
              }`} />
            </div>
            <div>
              <p className="font-semibold text-navy-500">
                Drop your proposal here
              </p>
              <p className="text-gray-600 text-sm">or click to browse files</p>
            </div>
            <div className="flex items-center justify-center space-x-4 text-xs text-gray-600">
              <span>PDF</span>
              <span>•</span>
              <span>Word</span>
              <span>•</span>
              <span>Max 10MB</span>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="flex items-center space-x-2 text-error-600 bg-error-50 p-3 rounded-lg border border-error-100">
          <AlertCircle className="h-4 w-4" />
          <span className="text-sm">{error}</span>
        </div>
      )}
    </div>
  );
};

export default FileUpload;