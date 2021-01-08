import string
class LoyaltyPartnerChecker:
    def __init__(self, loyalty_partner_name, member_id):
        self.loyalty_partner_name = loyalty_partner_name.lower()
        self.member_id = member_id
        
    def verify_member_id(self):
        member_id = self.member_id
        if self.loyalty_partner_name != "Millennium Rewards".lower():
            try:
                int(member_id)
            except:
                return False
        if (
            self.loyalty_partner_name == "GoJet Points".lower()
            and len(member_id) < 10
            or len(member_id) > 16
        ):
            return False
        elif (
            self.loyalty_partner_name == "IndoPacific Miles".lower()
            and len(member_id) != 10
        ):
            return False
        elif (
            self.loyalty_partner_name == "Eminent Airways Guest".lower()
            and len(member_id) != 12
        ):
            return False
        elif (
            self.loyalty_partner_name == "Quantum Airlines QFlyer".lower()
            and len(member_id) != 10
        ):
            return False
        elif (
            self.loyalty_partner_name == "Conrad X Club".lower()
            and len(member_id) != 9
        ):
            return False
        elif self.loyalty_partner_name == "Millennium Rewards".lower():
            if len(member_id) != 10:
                return False
            try:
                int(member_id[:9])
            except:
                return False
            if member_id[9:10] not in string.ascii_letters:
                return False
        return True