"""
Metrics service for tracking usage and performance.
"""
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class MetricsRecord(Base):
    """Database model for metrics tracking."""
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    event_type = Column(String(50), index=True)  # upload, analysis, generation
    organization_name = Column(String(255))
    decline_reason = Column(String(50))
    processing_time_ms = Column(Float)
    file_size_bytes = Column(Integer)
    proposal_word_count = Column(Integer)
    user_session_id = Column(String(100))
    error_message = Column(Text, nullable=True)
    llm_provider = Column(String(20))
    llm_tokens_used = Column(Integer)

class MetricsService:
    """Service for tracking and retrieving metrics."""
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize metrics service.
        
        Args:
            database_url: Database connection string
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "sqlite:///./metrics.db"  # Default to SQLite for development
        )
        
        # Create engine and session
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def track_upload(
        self,
        organization_name: str,
        file_size: int,
        word_count: int,
        processing_time_ms: float,
        session_id: str
    ) -> None:
        """
        Track a file upload event.
        
        Args:
            organization_name: Name of the organization
            file_size: Size of uploaded file in bytes
            word_count: Number of words in proposal
            processing_time_ms: Time taken to process
            session_id: User session identifier
        """
        try:
            with self.SessionLocal() as db:
                metric = MetricsRecord(
                    event_type="upload",
                    organization_name=organization_name,
                    file_size_bytes=file_size,
                    proposal_word_count=word_count,
                    processing_time_ms=processing_time_ms,
                    user_session_id=session_id
                )
                db.add(metric)
                db.commit()
        except Exception as e:
            logger.error(f"Error tracking upload metric: {e}")
    
    def track_analysis(
        self,
        organization_name: str,
        processing_time_ms: float,
        session_id: str,
        llm_provider: str = "openai",
        tokens_used: int = 0
    ) -> None:
        """
        Track a proposal analysis event.
        
        Args:
            organization_name: Name of the organization
            processing_time_ms: Time taken to analyze
            session_id: User session identifier
            llm_provider: AI provider used
            tokens_used: Number of tokens consumed
        """
        try:
            with self.SessionLocal() as db:
                metric = MetricsRecord(
                    event_type="analysis",
                    organization_name=organization_name,
                    processing_time_ms=processing_time_ms,
                    user_session_id=session_id,
                    llm_provider=llm_provider,
                    llm_tokens_used=tokens_used
                )
                db.add(metric)
                db.commit()
        except Exception as e:
            logger.error(f"Error tracking analysis metric: {e}")
    
    def track_generation(
        self,
        organization_name: str,
        decline_reason: str,
        processing_time_ms: float,
        session_id: str,
        llm_provider: str = "openai",
        tokens_used: int = 0
    ) -> None:
        """
        Track a memo generation event.
        
        Args:
            organization_name: Name of the organization
            decline_reason: Reason for decline
            processing_time_ms: Time taken to generate
            session_id: User session identifier
            llm_provider: AI provider used
            tokens_used: Number of tokens consumed
        """
        try:
            with self.SessionLocal() as db:
                metric = MetricsRecord(
                    event_type="generation",
                    organization_name=organization_name,
                    decline_reason=decline_reason,
                    processing_time_ms=processing_time_ms,
                    user_session_id=session_id,
                    llm_provider=llm_provider,
                    llm_tokens_used=tokens_used
                )
                db.add(metric)
                db.commit()
        except Exception as e:
            logger.error(f"Error tracking generation metric: {e}")
    
    def track_error(
        self,
        event_type: str,
        error_message: str,
        session_id: str
    ) -> None:
        """
        Track an error event.
        
        Args:
            event_type: Type of operation that failed
            error_message: Error description
            session_id: User session identifier
        """
        try:
            with self.SessionLocal() as db:
                metric = MetricsRecord(
                    event_type=f"error_{event_type}",
                    error_message=error_message,
                    user_session_id=session_id
                )
                db.add(metric)
                db.commit()
        except Exception as e:
            logger.error(f"Error tracking error metric: {e}")
    
    def get_summary_metrics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get summary metrics for the specified period.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Dictionary containing summary metrics
        """
        try:
            with self.SessionLocal() as db:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                # Total counts
                total_uploads = db.query(func.count(MetricsRecord.id)).filter(
                    MetricsRecord.event_type == "upload",
                    MetricsRecord.timestamp >= cutoff_date
                ).scalar()
                
                total_generations = db.query(func.count(MetricsRecord.id)).filter(
                    MetricsRecord.event_type == "generation",
                    MetricsRecord.timestamp >= cutoff_date
                ).scalar()
                
                # Average processing times
                avg_analysis_time = db.query(func.avg(MetricsRecord.processing_time_ms)).filter(
                    MetricsRecord.event_type == "analysis",
                    MetricsRecord.timestamp >= cutoff_date
                ).scalar() or 0
                
                avg_generation_time = db.query(func.avg(MetricsRecord.processing_time_ms)).filter(
                    MetricsRecord.event_type == "generation",
                    MetricsRecord.timestamp >= cutoff_date
                ).scalar() or 0
                
                # Most common decline reasons
                decline_reasons = db.query(
                    MetricsRecord.decline_reason,
                    func.count(MetricsRecord.id).label('count')
                ).filter(
                    MetricsRecord.event_type == "generation",
                    MetricsRecord.timestamp >= cutoff_date,
                    MetricsRecord.decline_reason.isnot(None)
                ).group_by(
                    MetricsRecord.decline_reason
                ).order_by(
                    func.count(MetricsRecord.id).desc()
                ).limit(5).all()
                
                # Error rate
                total_errors = db.query(func.count(MetricsRecord.id)).filter(
                    MetricsRecord.event_type.like("error_%"),
                    MetricsRecord.timestamp >= cutoff_date
                ).scalar()
                
                # Unique sessions
                unique_sessions = db.query(func.count(func.distinct(MetricsRecord.user_session_id))).filter(
                    MetricsRecord.timestamp >= cutoff_date
                ).scalar()
                
                return {
                    "period_days": days,
                    "total_uploads": total_uploads,
                    "total_generations": total_generations,
                    "unique_sessions": unique_sessions,
                    "average_analysis_time_ms": round(avg_analysis_time, 2),
                    "average_generation_time_ms": round(avg_generation_time, 2),
                    "top_decline_reasons": [
                        {"reason": reason, "count": count}
                        for reason, count in decline_reasons
                    ],
                    "error_count": total_errors,
                    "error_rate": round((total_errors / (total_uploads + 1)) * 100, 2)
                }
                
        except Exception as e:
            logger.error(f"Error getting summary metrics: {e}")
            return {
                "error": "Failed to retrieve metrics",
                "period_days": days
            }
    
    def get_daily_metrics(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get daily metrics for the specified period.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of daily metric dictionaries
        """
        try:
            with self.SessionLocal() as db:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                daily_metrics = db.query(
                    func.date(MetricsRecord.timestamp).label('date'),
                    func.count(func.distinct(MetricsRecord.user_session_id)).label('unique_users'),
                    func.count(MetricsRecord.id).filter(
                        MetricsRecord.event_type == "upload"
                    ).label('uploads'),
                    func.count(MetricsRecord.id).filter(
                        MetricsRecord.event_type == "generation"
                    ).label('generations')
                ).filter(
                    MetricsRecord.timestamp >= cutoff_date
                ).group_by(
                    func.date(MetricsRecord.timestamp)
                ).order_by(
                    func.date(MetricsRecord.timestamp).desc()
                ).all()
                
                return [
                    {
                        "date": str(metric.date),
                        "unique_users": metric.unique_users,
                        "uploads": metric.uploads or 0,
                        "generations": metric.generations or 0
                    }
                    for metric in daily_metrics
                ]
                
        except Exception as e:
            logger.error(f"Error getting daily metrics: {e}")
            return []