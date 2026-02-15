"""Premium feature management for Bayon Trip Logger."""

class PremiumTier:
    """Manages premium feature access."""
    
    FREE_FEATURES = {
        "basic_metrics": True,
        "map_view": True,
        "single_trip": True,
    }
    
    PREMIUM_FEATURES = {
        "advanced_analytics": True,
        "ai_insights": True,
        "trip_comparison": True,
        "export_pdf": True,
        "export_data": True,
        "acceleration_heatmap": True,
        "driving_style_classification": True,
    }
    
    def __init__(self, is_premium=False):
        self.is_premium = is_premium
    
    def has_feature(self, feature_name):
        """Check if a feature is available."""
        if feature_name in self.FREE_FEATURES:
            return True
        if feature_name in self.PREMIUM_FEATURES:
            return self.is_premium
        return False
    
    def get_feature_description(self, feature_name):
        """Get description for a premium feature."""
        descriptions = {
            "advanced_analytics": "Detailed acceleration heatmaps and jerk analysis",
            "ai_insights": "AI-powered driving style classification and recommendations",
            "trip_comparison": "Compare multiple trips side-by-side",
            "export_pdf": "Export beautiful PDF reports of your trips",
            "export_data": "Export processed data in multiple formats",
            "acceleration_heatmap": "Visual heatmap of acceleration patterns",
            "driving_style_classification": "ML-based classification of your driving style",
        }
        return descriptions.get(feature_name, "Premium feature")
