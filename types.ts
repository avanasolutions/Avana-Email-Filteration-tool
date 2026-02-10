export interface ProcessedDomain {
  domain: string;
  emails: string[];
  selectedEmails: string[];
  matchCount: number;
}

export interface ProcessingStats {
  totalEmailsFound: number;
  totalDomains: number;
  totalSelected: number;
}

export interface RoleConfig {
  keywords: string[];
}

export enum ProcessingState {
  IDLE = 'IDLE',
  ANALYZING = 'ANALYZING',
  COMPLETE = 'COMPLETE',
  ERROR = 'ERROR'
}
